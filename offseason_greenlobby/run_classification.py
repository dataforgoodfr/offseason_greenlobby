import argparse
import os
import time


from modeling.open_ai import OpenAIModel
from modeling.mistral import MistralModel
from modeling.embedding import Embedding
from utils.data_loader import load_data
from utils.data_loader import load_prompt
from config import DATA_DIR,COL_DESCRIPTION,COL_IDEES,COL_EXPOSE_SOMMAIRE
import argparse
import pandas as pd
from config import COL_LABEL,COL_PREDICTIONS,METRICS
from evaluation.metrics import evaluate_classification
from utils.utils import list_of_strings
import os.path
from sklearn.metrics import confusion_matrix
from datetime import datetime

import sys
sys.path.append("/Users/basileroth/Desktop/Code/offseason_greenlobby")
import importlib




def main(model_name, provider, input_file, prompt, batch_size, delay, temperature,metrics_param, output_file_eval, output_file_pred):
    
    # Process dataframes
    data = load_data(input_file)

    # Parse data
    idees = data[COL_IDEES].tolist()     # Idees
    exposesommaire = data[COL_EXPOSE_SOMMAIRE].tolist()     # Idees
    description = data[COL_DESCRIPTION].tolist()     # Description

    # Select a model provider
    if provider == 'openai':
        model = OpenAIModel(model_name)
    elif provider == 'mistral':
        model = MistralModel(model_name)
    elif provider == "embedding" :
        model = Embedding(model_name)
    else:
        raise ValueError("Unsupported provider (you need to pick either openai or mistral)")

    # Build prompt
    # prompt_json = load_prompt(prompt)         # OLD

    module_name = "data.prompts.prompts_py"       # Name of the module as a string
    variable_name = prompt # Name of the variable as a string
    module = importlib.import_module(module_name)
    value = getattr(module, variable_name)
    prompt_json = value

    # Classification des exposés sommaire en fonction de l'idée
    if batch_size > 0:
        # WITH BATCH
        start = time.time()
        predictions = model.classify_batches(data, batch_size, prompt_json["template"],delay,temperature=temperature)
        end = time.time()
        print(f"Total execution time: {end - start:.5f} seconds")

    # NO BATCH
    else:
        start = time.time()
        if provider == "embedding" :
            model.prompt_encode(description[0])

            predictions = [
                model.classify(expo) for id,expo,descr in zip(idees,exposesommaire,description)
                ]
            
        else:
            predictions = [
                model.classify(
                    prompt_json.format(
                        IDEE=id,
                        DESCRIPTION=descr,
                        EXPOSE_SOMMAIRE=expo
                    ),
                    temperature=temperature) for id,expo,descr in zip(idees,exposesommaire,description)
                ]
        end = time.time()
        EXEC_TIME = end - start
        print(f"Total execution time: {end - start:.5f} seconds")

    
    # Save prompt and predictions
    data['prediction'] = predictions
    data['llm_provider'] = provider
    data['model'] = model_name
    data['prompt_content'] = [prompt_json.format(
                    IDEE=id,
                    DESCRIPTION=descr,
                    EXPOSE_SOMMAIRE=expo
                ) for id,expo,descr in zip(idees,exposesommaire,description)]
    data['prompt_name'] = prompt

    # Save to prediction file
    data.to_csv(DATA_DIR / output_file_pred, index=False)
    print(f"Predictions saved to {output_file_pred}")

    # Evaluation
    if COL_LABEL in data.columns:
        y_true = data[COL_LABEL].str.lower()
        y_pred = data[COL_PREDICTIONS].str.lower()
        y_true = [str(x) for x in y_true]
        y_pred = [str(x) for x in y_pred]

        # Compute the desired metrics 
        metrics = evaluate_classification(y_true, y_pred)

        metrics["confusion_matrix"] = [confusion_matrix(y_pred=y_pred,y_true=y_true,labels=["oui","non"])]
        metrics["prompt"] = [data['prompt_name'].values[0]]
        metrics["model"] = [model_name]
        metrics["temperature"] = [temperature]
        metrics["y_true"] = [y_true]
        metrics["y_pred"] = [y_pred]
        metrics["execution_time"] = [EXEC_TIME]
        metrics["time_eval"] = [datetime.now()]

        # Plot
        print("Confusion matrix:")
        print(confusion_matrix(y_pred=y_pred,y_true=y_true,labels=["oui","non"]))
        for metric in metrics_param:
            print(f"{metric}: {metrics[metric][0]:.4f}")

        # If the file already exists
        if os.path.isfile(output_file_eval):
            df_res = pd.read_csv(
                output_file_eval)
            for metric, value in metrics.items():
                metrics[metric] = value[0]
            df_res.loc[-1] = metrics
            df_res.to_csv(output_file_eval,index=0)
        # Else create it
        else:
            pd.DataFrame.from_dict(metrics).to_csv(
                output_file_eval,
                index=0,)

if __name__ == "__main__":
    """
    main
    """
    parser = argparse.ArgumentParser(description="Run text classification using LLMs.")

    parser.add_argument('--model_name', type=str, required=True, help='Model name to use.')
    parser.add_argument('--provider', type=str, choices=['openai', 'mistral','embedding'], required=True, help='LLM provider.')
    parser.add_argument('--prompt', type=str, required=True, help='Select a prompt in the Json file containing the prompts [data/prompts/prompts_py.py]')
    parser.add_argument('--batch_size', type=str, default=0, help='Select a batch size ')
    parser.add_argument('--delay', type=str, default=0, help='Delay to wait between batches')
    parser.add_argument('--input_file', type=str, required=True, help='Path to input CSV file. Columns = [IDEES,DESCRIPTION,NOM_AMENDEMENT,LABEL]')
    parser.add_argument('--output_file_pred', type=str, required=True, help='Path to save predictions.')
    parser.add_argument('--output_file_eval', type=str, default="../data/results/eval/evaluations.csv", help='Output file')
    parser.add_argument('--temperature', type=str, default=0, help='Temperature of model.')
    parser.add_argument('--metrics_param', type=list_of_strings, default=METRICS, help='List of metrics to plot. Default ["accuracy", "precision", "recall","f1_score"]')

    args = parser.parse_args()

    main(
        model_name=args.model_name, 
        provider = args.provider,
        input_file = args.input_file,
        prompt = args.prompt, 
        batch_size = int(args.batch_size),
        delay = int(args.delay),
        temperature = float(args.temperature),
        metrics_param = args.metrics_param,
        output_file_eval = args.output_file_eval,
        output_file_pred = args.output_file_pred,)