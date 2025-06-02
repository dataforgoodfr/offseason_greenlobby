# Define a custom argument type for a list of strings
def list_of_strings(arg):
    return arg.split(',')


import json
import re
from typing import List, Tuple
import html

def get_gp(folder,gp):

    with open(folder + gp + '.json') as f:
        d = json.load(f)
        return d['libelleAbrege']
    
def get_gp_nom(folder,gp):

    with open(folder + gp + '.json') as f:
        d = json.load(f)
        return d['libelle']
    

def get_id_nom(folder,acteur):
    print(folder)
    with open(folder + acteur + '.json') as f:
        d = json.load(f)
        return d['etatCivil']['ident']['nom']
    
def get_id_prenom(folder,acteur):
    with open(folder + acteur + '.json') as f:
        d = json.load(f)
        return d['etatCivil']['ident']['prenom']
            

def clean_text(text):
    """ Nettoie le texte HTML pour le rendre plus lisible pour un humain. """
    decoded_text = html.unescape(text)
    clean_text = re.sub(r'<[^>]*>', '', decoded_text)
    clean_text = clean_text.replace('«', '"').replace('»', '"')
    clean_text = clean_text.replace(u'\xa0', ' ')
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
    return clean_text

import re

def cleaned_text(text):
    first = re.sub(r'[^\w\s]+', '', text)
    cleaned_text = re.sub(r'\s+', ' ', first).strip()
    return cleaned_text

import re
from typing import List, Tuple

def get_surrounding_words(text: str, substring: str, window: int = 10) -> Tuple[List[str], List[str]]:
    """
    Recherche la première occurrence de `substring` dans `text` et renvoie
    deux listes : les `window` mots précédant la chaîne et les `window` mots suivant la chaîne.
    """
    match = re.search(substring.lower(), text.lower())
    if not match:
        return [], []

    start_idx, end_idx = match.span()

    # Extraire tous les mots (\w+) avec leurs positions dans le texte
    mots_spans = [(m.group(), m.span()) for m in re.finditer(r"\w+", text.lower())]
    mots = [mot for mot, _ in mots_spans]

    # Trouver l’indice du mot couvrant le début de la sous-chaîne
    first_word_index = None
    for idx, (_, span) in enumerate(mots_spans):
        if span[1] > start_idx:
            first_word_index = idx
            break
    if first_word_index is None:
        return [], []

    # Trouver l’indice du mot couvrant la fin de la sous-chaîne
    last_word_index = None
    for idx in range(first_word_index, len(mots_spans)):
        if mots_spans[idx][1][0] >= end_idx:
            last_word_index = idx
            break
    if last_word_index is None:
        last_word_index = len(mots) - 1

    # Sélectionner les window mots avant et après
    start_context = max(0, first_word_index - window)
    end_context = min(len(mots), last_word_index + window + 1)

    mots_avant = ' '.join(mots[start_context:first_word_index]) + " " + substring + " " + ' '.join(mots[last_word_index :end_context])

    return mots_avant


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
