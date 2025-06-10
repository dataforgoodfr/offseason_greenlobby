import pandas as pd

import sys
sys.path.append('/Users/basileroth/Desktop/Code/offseason_greenlobby/')
from offseason_greenlobby.config import color_16
import numpy as np
# define subplot grid
import matplotlib.pyplot as plt 
import re

from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

tokenizer = AutoTokenizer.from_pretrained(
    "Jean-Baptiste/camembert-ner")

model = AutoModelForTokenClassification.from_pretrained("Jean-Baptiste/camembert-ner")



str_influence_lobbys = [
    "amendement est proposé par",
    "amendement a été proposé par",
    "amendement est proposé en concertation avec",
    "proposé ici par",
    "amendement proposé par",    
    "amendement a été travaillé avec",
    "amendement travaillé avec",
    "amendement travaillé en coopération avec"
    "amendement travaillé",
    "travaillé avec",
    "a été travaillé avec",
    "travaillé en coopération avec",
    "amendement a été co-construit en collaboration avec",
    "a été rédigé en collaboration avec",
    "rédigé en collaboration avec",
    "amendement a été rédigé en collaboration avec",
    "amendement rédigé en collaboration",
    "amendement est issu d'une proposition de",
    "inspiré de l'une des propositions de"
    ]

def matcher(x):
    for i in str_influence_lobbys:
        if i.lower() in x.lower():
            return i
    else:
        return np.nan


def extract_until_period(text: str, search: str) -> str:
    """
    Finds the first occurrence of `search` in `text` and returns the following
    characters up to (but not including) the next period.
    
    If the search string is not found or there's no period after it, returns an empty string.
    """
    search_index = text.find(search)
    if search_index == -1:
        return ""  # Search string not found

    # Find the previous period before the search string
    prev_period_index = text.rfind(".", 0, search_index)
    start = prev_period_index + 1 if prev_period_index != -1 else 0

    # Find the next period after the search string
    next_period_index = text.find(".", search_index)
    end = next_period_index + 1 if next_period_index != -1 else len(text)

    return text[start:end].strip()

import string

def detect_organizations(df):

    df['Match'] = df["EXPOSE_SOMMAIRE"].apply(matcher)
    df_lobbys = df.dropna(subset=['Match']).copy().reset_index(drop=True)
    df_lobbys['Match_Str'] = df_lobbys.apply(lambda x : extract_until_period(x['EXPOSE_SOMMAIRE'], x['Match']), axis=1)

    nlp_tf = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")

    df_lobbys["lobbys"] = ""

    for index,row in df_lobbys.iterrows():
        phrase = row['Match_Str']
        # TRANSFORMERS
        phrase = phrase.translate(str.maketrans('', '', string.punctuation))
        entities = nlp_tf(phrase)

        orgs_tf = [ent['word'] for ent in entities if ent['entity_group'] == "ORG"]
        df_lobbys.iloc[index,-1] = str(orgs_tf)

    return df_lobbys