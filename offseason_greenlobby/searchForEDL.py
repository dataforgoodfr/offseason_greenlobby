import os
import json
import html
import pandas as pd
from collections import defaultdict

# Configuration
DOSSIERS_JSON = ["DLR5L16N49726/PRJLANR5L16B2436", "DLR5L16N49726/PRJLANR5L16BTC2600"]
CSV_PATH = "phrases_fusionnees_ordonnees.csv"
OUTPUT_CSV = "result_comptage.csv"

# --- Lecture du CSV de départ ---
df = pd.read_csv(CSV_PATH, encoding='latin1')
search_phrases = df.iloc[:, 1].tolist()  # 2e colonne : les chaînes à chercher

# --- Initialisation des résultats ---
results = {phrase: defaultdict(int) for phrase in search_phrases}
fichiers_par_groupe = defaultdict(int)

# --- Parcours des fichiers JSON ---
for dossier in DOSSIERS_JSON:
    for filename in os.listdir(dossier):
        if filename.endswith(".json"):
            path = os.path.join(dossier, filename)
            try:
                with open(path, 'r', encoding='latin1') as f:
                    data = json.load(f)
                    amendement = data.get("amendement", {})

                    expose_raw = amendement.get("corps", {}).get("contenuAuteur", {}).get("exposeSommaire", "")
                    expose_clean = html.unescape(expose_raw)

                    groupe = amendement.get("signataires", {}).get("auteur", {}).get("groupePolitiqueRef")
                    groupes = [groupe] if isinstance(groupe, str) else groupe or []

                    # Comptage des fichiers par groupe
                    for g in groupes:
                        fichiers_par_groupe[g] += 1

                    # Comptage des occurrences par phrase
                    for phrase in search_phrases:
                        count = expose_clean.lower().count(phrase.lower())
                        if count > 0:
                            for g in groupes:
                                results[phrase][g] += count

            except Exception as e:
                print(f"Erreur dans le fichier {filename} : {e}")

# --- Création du DataFrame enrichi ---
df_result = df.copy()
groupes_uniques = sorted({g for phrase_result in results.values() for g in phrase_result})

# Ajouter les colonnes dynamiquement
for g in groupes_uniques:
    df_result[g] = 0

for idx, phrase in enumerate(search_phrases):
    for g in results[phrase]:
        df_result.at[idx, g] = results[phrase][g]

# --- Sauvegarde du fichier CSV ---
df_result.to_csv(OUTPUT_CSV, index=False)
print(f"✅ Fichier enrichi enregistré : {OUTPUT_CSV}")

# --- Affichage résumé global ---
print("\n📊 Résumé du nombre de fichiers associés par groupe politique :")
for g, count in fichiers_par_groupe.items():
    print(f"  ➤ Total {g} : {count} fichiers associés")
