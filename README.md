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


### 2. .....

