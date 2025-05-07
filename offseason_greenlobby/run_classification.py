import argparse
import os
import time


from modeling.open_ai import OpenAIModel
from modeling.mistral import MistralModel
from utils.data_loader import load_data
from utils.data_loader import load_prompt
from config import DATA_DIR,COL_DESCRIPTION,COL_IDEES,COL_LABEL,COL_NOM_AMENDEMENT

def main(model_name, provider, input_file, output_file, prompt, batch_size, delay, temperature):
    
    # Process dataframes
    data = load_data(input_file)

    # Parse data
    idees = data[COL_IDEES].tolist()     # Idees
    exposesommaire = data[COL_NOM_AMENDEMENT].tolist()     # Idees
    description = data[COL_DESCRIPTION].tolist()     # Description
    labels = data[COL_LABEL].tolist()     # Label

    # Select a model provider
    if provider == 'openai':
        model = OpenAIModel(model_name)
    elif provider == 'mistral':
        model = MistralModel(model_name)
    else:
        raise ValueError("Unsupported provider (you need to pick either openai or mistral)")

    # Build prompt
    prompt_json = load_prompt(prompt)

    # Classification des exposés sommaire en fonction de l'idée
    if batch_size > 0:
        # WITH BATCH
        start = time.time()
        predictions = model.classify_batches(data, batch_size, prompt_json["template"],delay,temperature=temperature)
        end = time.time()
        print(f"Total execution time: {end - start:.5f} seconds")

    else:
        start = time.time()
        # NO BATCH
        if provider == "mistral":
            predictions = [
                model.classify(
                    prompt_json["template"].format(
                        EXPOSE_SOMMAIRE=id,
                        IDEE=expo,
                        DESCRIPTION=descr
                    ),
                    temperature=temperature) for id,expo,descr in zip(idees,exposesommaire,description)
                ]
            
        elif provider == "openai":
            predictions = [
                model.classify(
                    exposes_sommaires = [expo],
                    instruct_system = prompt_json["template"].format(
                        IDEE=id,
                        DESCRIPTION=descr
                    ),
                    temperature=temperature) for id,expo,descr in zip(idees,exposesommaire,description)
                ]
        

        end = time.time()
        print(f"Total execution time: {end - start:.5f} seconds")

    
    # Save prompt and predictions
    data['prediction'] = predictions
    data['prompt'] = [prompt_json["template"].format(EXPOSE_SOMMAIRE=id,IDEE=expo,DESCRIPTION=descr) for id,expo,descr in zip(idees,exposesommaire,description)]

    # Save to prediction file
    data.to_csv(DATA_DIR / output_file, index=False)
    print(f"Predictions saved to {output_file}")

if __name__ == "__main__":
    """
    main
    """
    parser = argparse.ArgumentParser(description="Run text classification using LLMs.")

    parser.add_argument('--model_name', type=str, required=True, help='Model name to use.')
    parser.add_argument('--provider', type=str, choices=['openai', 'mistral'], required=True, help='LLM provider.')
    parser.add_argument('--prompt', type=str, required=True, help='Select a prompt in the Json file containing the prompts [data/prompts/prompts.json]')
    parser.add_argument('--batch_size', type=str, default=0, help='Select a batch size ')
    parser.add_argument('--delay', type=str, default=0, help='Delay to wait between batches')
    parser.add_argument('--input_file', type=str, required=True, help='Path to input CSV file. Columns = [IDEES,DESCRIPTION,NOM_AMENDEMENT,LABEL]')
    parser.add_argument('--output_file', type=str, required=True, help='Path to save predictions.')
    parser.add_argument('--temperature', type=str, default=0, help='Temperature of model.')

    args = parser.parse_args()

    main(args.model_name, args.provider, args.input_file, args.output_file, args.prompt, int(args.batch_size), int(args.delay), int(args.temperature))

