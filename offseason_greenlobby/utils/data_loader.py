import pandas as pd
from config import AMENDEMENTS_DIR,DATA_DIR,COL_NOM_AMENDEMENT,COL_EXPOSE_SOMMAIRE
from config import DATA_DIR
import json

def load_data(file_path: str):
    """
    
    """

    # Load dataframe with amendements
    try:
        amendements_df = pd.read_csv(AMENDEMENTS_DIR)
    except Exception as e:
        print(f"An error occured while loading the dataframe: {e}")

    # Load labelled df
    labelled_df = pd.read_csv(DATA_DIR / file_path)

    if COL_EXPOSE_SOMMAIRE not in labelled_df.columns:
        # Merge both 
        merged_df = pd.merge(
            amendements_df, 
            labelled_df, 
            left_on=COL_NOM_AMENDEMENT, 
            right_on=COL_NOM_AMENDEMENT, how='inner')
        
        print("Number of samples to classify: ",merged_df.shape[0])
        return merged_df
    else:
        print("Number of samples to classify: ",labelled_df.shape[0])
        return labelled_df


def load_prompt(prompt_name: str):
    """
    LOAD PROMPT FROM A JSON FILE
    """
    with open(DATA_DIR / "prompts/prompts.json", "r", encoding="utf-8") as f:
        prompt_data = json.load(f)

        return prompt_data[prompt_name]
    

def load_prompt_py(prompt_name: str):
    """
    LOAD PROMPT FROM A PYTHON FILE
    """
    with open(DATA_DIR / "prompts/prompts.json", "r", encoding="utf-8") as f:
        prompt_data = json.load(f)

        return prompt_data[prompt_name]

