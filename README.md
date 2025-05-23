# offseason_greenlobby

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

Recherche d'éléments de language dans les amendements apportés par différents partis politique sur des projets de loi.


## Steps to use code base

Follow these steps to be able to run the code.

### 1. Set API keys as environment vars

If you want to run experiments using either LLM providers (MistralAI or OpenAI), you will need to use an API_KEY.

You need to use environment variables to set those:
- `OPENAI_API_KEY`
- `MISTRAL_API_KEY`

To add your OpenAI/Mistral API key as an environment variable, follow these steps depending on your operating system and environment:

---

#### 🖥️ For Unix/Linux/macOS (Terminal or Server)

###### Temporarily (only for the current session)

```bash
export OPENAI_API_KEY="your-api-key-here"
```

###### Permanently (for all sessions)

1. Open your shell profile config file (e.g., `~/.bashrc`, `~/.zshrc`, or `~/.bash_profile`) in a text editor:

   ```bash
   nano ~/.bashrc  # or ~/.zshrc for Zsh users
   ```
2. Add the line:

   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```
3. Save and exit, then apply changes:

   ```bash
   source ~/.bashrc  # or source ~/.zshrc
   ```
### 2. Install requirements

Next it is required to install the different dependencies required to run the code. 

   ```bash
   pip install -r requirements.txt
   ```

### 3. Run code

### 3.1 Classification

To run the classification script you need to locate yourself in the `offseason_greenlobby/offseason_greenlobby/` folder. 

```bash
   cd offseason_greenlobby
   ```

Then you need to run the `run_classification.py` script using python. 

The important parts are:
- The prompt to be used has to be stored in the `data/prompts/prompts.json` file with a specific name.
- The labeled dataset needs to have a specific format: `IDEES`,`DESCRIPTION`,`NOM_AMENDEMENT`,`LABEL`.

Here is an example of how to do it with some parameters:

```bash
python run_classification.py \                                                                                   
    --model_name gpt-4 \
    --provider openai \
    --prompt prompt_test \
    --batch_size 0 \
    --delay 0 \
    --input_file processed/lb_dataset.csv \
    --output_file_pred ../data/results/predictions/gpt4turbo_prompt_test.csv
```

Here is the help from this command to get the detailled view of the parameters to be used:

```bash
usage: run_classification.py [-h] --model_name MODEL_NAME --provider {openai,mistral} --prompt PROMPT [--batch_size BATCH_SIZE] [--delay DELAY] --input_file INPUT_FILE
                             --output_file_pred OUTPUT_FILE_PRED [--output_file_eval OUTPUT_FILE_EVAL] [--temperature TEMPERATURE] [--metrics_param METRICS_PARAM]

Run text classification using LLMs.

options:
  -h, --help            show this help message and exit
  --model_name MODEL_NAME
                        Model name to use.
  --provider {openai,mistral}
                        LLM provider.
  --prompt PROMPT       Select a prompt in the Json file containing the prompts [data/prompts/prompts.json]
  --batch_size BATCH_SIZE
                        Select a batch size
  --delay DELAY         Delay to wait between batches
  --input_file INPUT_FILE
                        Path to input CSV file. Columns = [IDEES,DESCRIPTION,NOM_AMENDEMENT,LABEL]
  --output_file_pred OUTPUT_FILE_PRED
                        Path to save predictions.
  --output_file_eval OUTPUT_FILE_EVAL
                        Output file
  --temperature TEMPERATURE
                        Temperature of model.
  --metrics_param METRICS_PARAM
                        List of metrics to plot. Default ["accuracy", "precision", "recall","f1_score"]
```

    
### 3.2 Evaluate Results 

To run the evaluation script you need to locate yourself in the `offseason_greenlobby/offseason_greenlobby/` folder. Same as previously.

```bash
   cd offseason_greenlobby
   ```

Then you need to run the `run_eval_script.py` script using python. 

The important parts are:
- You need to provide the path to the previous output file that was generated. i.e.: `./data/results/predictions/mistral_predictions.csv`.

Here is an example of how to do it with some parameters:

```bash
python run_eval_script.py \
    --predictions_file ../data/results/predictions/mistral_predictions.csv \
    --verbose True \
    --save True \
    --output_file ../data/results/eval/evaluations.csv \
```

Here is the help from this command to get the detailled view of the parameters to be used:

```bash
python run_eval_script.py -h
usage: run_eval_script.py [-h] --predictions_file PREDICTIONS_FILE [--metrics_param METRICS_PARAM] [--verbose VERBOSE] [--save SAVE]
                          [--output_file OUTPUT_FILE]

Evaluate classification results.

options:
  -h, --help            show this help message and exit
  --predictions_file PREDICTIONS_FILE
                        Path to predictions CSV file.
  --metrics_param METRICS_PARAM
                        List of metrics to plot. Default ["accuracy", "precision", "recall","f1_score"]
  --verbose VERBOSE     Boolean to plot or not to plot
  --save SAVE           Decision to save evaluation output to output file.
  --output_file OUTPUT_FILE
                        Output file
```

