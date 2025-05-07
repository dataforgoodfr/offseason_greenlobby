# offseason_greenlobby

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

Recherche d'éléments de language dans les amendements apportés par différents partis politique sur des projets de loi.


## Project Organization

```
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default mkdocs project; see www.mkdocs.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── pyproject.toml     <- Project configuration file with package metadata for 
│                         offseason_greenlobby and configuration for tools like black
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.cfg          <- Configuration file for flake8
│
└── offseason_greenlobby   <- Source code for use in this project.
    │
    ├── __init__.py             <- Makes offseason_greenlobby a Python module
    │
    ├── config.py               <- Store useful variables and configuration
    │
    ├── dataset.py              <- Scripts to download or generate data
    │
    ├── features.py             <- Code to create features for modeling
    │
    ├── modeling                
    │   ├── __init__.py 
    │   ├── predict.py          <- Code to run model inference with trained models          
    │   └── train.py            <- Code to train models
    │
    └── plots.py                <- Code to create visualizations
```

## Run code

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

##### 3.1 Classification

To run the classification script you need to locate yourself in the `offseason_greenlobby/offseason_greenlobby/` folder. 

```bash
   cd offseason_greenlobby
   ```

Then you need to run the `run_classification.py` script using python. 

Here is an example of how to do it with some parameters:

```bash
python run_classification.py \
    --model_name gpt-3.5-turbo \
    --provider openai \
    --prompt openai_1 \
    --batch_size 3 \
    --delay 0 \
    --input_file processed/labeled_idees_1.csv \
    --output_file results/predictions/openai_predictions.csv
```

Here is the help from this command to get the detailled view of the parameters to be used:

```bash
usage: run_classification.py [-h] --model_name MODEL_NAME --provider {openai,mistral} --prompt PROMPT [--batch_size BATCH_SIZE] [--delay DELAY] --input_file INPUT_FILE --output_file OUTPUT_FILE
                             [--temperature TEMPERATURE]

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
                        Path to input CSV file. Columns = [Idées,Description,Listes des amendements,En faveur ]
  --output_file OUTPUT_FILE
                        Path to save predictions.
  --temperature TEMPERATURE
                        Temperature of model.
```

    
Evaluate results:

bash
Copier
Modifier
python scripts/evaluate_results.py \
    --predictions_file results/predictions/openai_predictions.csv \
    --labels_file data/labels.csv
