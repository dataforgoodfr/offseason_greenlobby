import os
import json
import csv
import html
import re
import argparse

def clean_text(text):
    """ Nettoie le texte HTML pour le rendre plus lisible pour un humain. """
    decoded_text = html.unescape(text)
    clean_text = re.sub(r'<[^>]*>', '', decoded_text)
    clean_text = clean_text.replace('«', '"').replace('»', '"')
    clean_text = clean_text.replace(u'\xa0', ' ')
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
    return clean_text

def article_match(article_courte, target_article):
    """Retourne True si article_courte correspond à l'article voulu, même s'il y a des zéros ou du texte autour."""
    pattern = rf'\b0*{re.escape(str(target_article))}\b'
    return bool(re.search(pattern, article_courte))

def extract_expose_sommaire(json_path, target_article):
    """Extrait le texte du champ 'exposeSommaire' d'un fichier JSON et identifie la raison s’il n’est pas retenu."""
    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            article_courte = data.get('amendement', {}).get('pointeurFragmentTexte', {}).get('division', {}).get('articleDesignationCourte', '')
            if not article_match(article_courte, target_article):
                return None, "Non article ciblé"
            expose = data.get('amendement', {}).get('corps', {}).get('contenuAuteur', {}).get('exposeSommaire', '')
            if not expose.strip():
                return None, "Article ciblé sans exposé"
            result = clean_text(expose)
            return result, "OK"
    except Exception as e:
        return None, f"Erreur: {e}"

def process_folder(input_folder, output_csv, target_article):
    with open(output_csv, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Nom du fichier', 'ExposeSommaire']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        count = 0
        for root, dirs, files in os.walk(input_folder):
            for file in files:
                if file.endswith('.json'):
                    json_path = os.path.join(root, file)
                    expose_sommaire, status = extract_expose_sommaire(json_path, target_article)
                    
                    if status == "OK":
                        writer.writerow({'Nom du fichier': file, 'ExposeSommaire': expose_sommaire})
                        print(f"[{count}] OK : {file}")
                        count += 1
                    elif status == "Non article ciblé":
                        print(f"⛔ Non article ciblé : {file}")
                    elif status == "Article ciblé sans exposé":
                        print(f"⚠️ Article ciblé mais pas d'exposé : {file}")
                    else:
                        print(f"❌ Erreur dans {file} : {status}")
        print(f"\nNombre total d'amendements article {target_article} avec exposé : {count}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extraction des exposés sommaires d’un article donné.")
    parser.add_argument("input_folder", help="Chemin du dossier contenant les fichiers JSON")
    parser.add_argument("output_csv", help="Chemin du fichier CSV de sortie")
    parser.add_argument("article", type=int, help="Numéro de l'article à filtrer")
    args = parser.parse_args()

    process_folder(args.input_folder, args.output_csv, args.article)
    print(f"Le fichier CSV a été généré avec succès : {args.output_csv}")
