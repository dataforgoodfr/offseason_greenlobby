import pandas as pd
import openai
import time
import os
from tqdm import tqdm

# Instancie un client OpenAI
client = openai.OpenAI(api_key='XXXX')

# Fichiers
input_file = '/Users/thibaut/Downloads/amendements.csv'
output_file = '/Users/thibaut/downloads/resultats_analyse.csv'

# Paramètres
batch_size = 10
sleep_time = 1  # Temps de repos entre les batchs
max_retries = 3  # Nombre d'essais API en cas d'échec
valid_responses = ["en faveur", "neutre", "opposé"]

# Chargement initial
if os.path.exists(output_file):
    result_df = pd.read_csv(output_file)
    print(f"Fichier existant détecté, {len(result_df)} amendements déjà traités.")
else:
    result_df = pd.DataFrame()

df = pd.read_csv(input_file)
df = df.dropna(subset=['ExposeSommaire']).reset_index(drop=True)

# Début à l'index correspondant
start_index = len(result_df)
print(f"Traitement à partir de l'index {start_index}")

# Prompt d'instruction
instruction_system = (
    "Tu es expert en analyse politique et en compréhension des mécanismes d'influence législative. "
    "Tu dois analyser des amendements par rapport à l'idée suivante : "
    '"limiter les délais de recours administratifs : accélérer les projets agricoles en réduisant les freins juridiques perçus comme des obstacles, '
    'en particulier les normes environnementales." '
    "Pour chaque amendement donné, réponds uniquement par : 'en faveur', 'neutre' ou 'opposé'. "
    "Ne donne aucune justification, seulement le terme demandé."
)

# Fonction d'appel API avec retry automatique
def batch_query(batch_texts):
    messages = [{"role": "system", "content": instruction_system}]
    for idx, amendement in enumerate(batch_texts):
        messages.append({
            "role": "user",
            "content": f"Amendement {idx+1} : {amendement}"
        })
    
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0,
                max_tokens=150,
            )
            content = response.choices[0].message.content.strip().lower()

            print("Réponse brute GPT :")
            print(content)

            # ✅ Nouveau découpage
            split_results = []
            for line in content.split("\n"):
                if ":" in line:
                    _, response_text = line.split(":", 1)
                    split_results.append(response_text.strip())

            # Validation
            results = []
            for res in split_results:
                res_clean = res.strip().lower()
                if res_clean in valid_responses:
                    results.append(res_clean)
                else:
                    results.append("réponse invalide")

            # Compléter si besoin
            while len(results) < len(batch_texts):
                results.append("réponse manquante")
            
            return results
        
        except Exception as e:
            print(f"Erreur API tentative {attempt+1}/{max_retries} : {e}")
            time.sleep((attempt + 1) * 5)
    return ["échec API"] * len(batch_texts)

# Boucle principale avec barre de progression
for i in tqdm(range(start_index, len(df), batch_size), desc="Traitement des amendements"):
    batch = df['ExposeSommaire'][i:i+batch_size].tolist()
    ids = df.index[i:i+batch_size].tolist()

    results = batch_query(batch)

    batch_df = pd.DataFrame({
        'Index': ids,
        'ExposeSommaire': batch,
        'ResultatAnalyse': results
    })
    
    result_df = pd.concat([result_df, batch_df], ignore_index=True)
    
    # Sauvegarde régulière
    result_df.to_csv(output_file, index=False)
    
    time.sleep(sleep_time)

print("✅ Analyse terminée.")
