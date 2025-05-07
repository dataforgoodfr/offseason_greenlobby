import pandas as pd
from config import AMENDEMENTS_DIR
from config import DATA_DIR
import json

def load_data(file_path: str):
    """
    
    """

    # Load dataframe with amendements
    amendements_df = pd.read_csv(AMENDEMENTS_DIR)

    # Load labelled df
    labelled_df = pd.read_csv(DATA_DIR / file_path)

    # Merge both 
    merged_df = pd.merge(
        amendements_df, 
        labelled_df, 
        left_on='Nom du fichier', 
        right_on='Listes des amendements', how='inner')
    
    print("Number of samples to classify: ",merged_df.shape[0])
    return merged_df


def load_prompt(prompt_name: str):
    """
    
    """
    with open(DATA_DIR / "prompts/prompts.json", "r", encoding="utf-8") as f:
        prompt_data = json.load(f)

        return prompt_data[prompt_name]

