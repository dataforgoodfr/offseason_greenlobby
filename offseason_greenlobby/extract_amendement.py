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
            # if not article_match(article_courte, target_article):
            #     return None, "Non article ciblé" , None , None , None
            expose = data.get('amendement', {}).get('corps', {}).get('contenuAuteur', {}).get('exposeSommaire', '')
            dispositif = data.get('amendement', {}).get('corps', {}).get('contenuAuteur', {}).get('dispositif', '')
            result = clean_text(expose)
            typeAuteur = data["amendement"]["signataires"]["auteur"]["typeAuteur"]
            typee = data["amendement"]["identification"]["prefixeOrganeExamen"]
            acteurRef = data["amendement"]["signataires"]["auteur"]["acteurRef"]
            groupePolitiqueRef = data["amendement"]["signataires"]["auteur"]["groupePolitiqueRef"]
            return result, "OK" , typeAuteur , acteurRef, groupePolitiqueRef, article_courte, typee, clean_text(dispositif)
    except Exception as e:
        return None, f"Erreur: {e}"

def process_folder(input_folder, output_csv, target_article):
    with open(output_csv, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Nom du fichier', 'ExposeSommaire','typeAuteur','acteurRef','groupePolitiqueRef','article_courte','type',"dispositif"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        count_ok = 0
        count_non_article_ciblé = 0
        count_cible_mais_sans_expose = 0
        count_erreur = 0

        count = 0
        for root, dirs, files in os.walk(input_folder):
            for file in files:
                if file.endswith('.json'):
                    json_path = os.path.join(root, file)
                    expose_sommaire, status, typeAuteur , acteurRef, groupePolitiqueRef, article_courte, typee,dispositif = extract_expose_sommaire(json_path, target_article)
                    
                    if status == "OK":
                        writer.writerow({'Nom du fichier': file, 
                                         'ExposeSommaire': expose_sommaire,
                                         'typeAuteur': typeAuteur,
                                         'acteurRef': acteurRef,
                                         'groupePolitiqueRef': groupePolitiqueRef,
                                         'article_courte': article_courte,
                                         'type': typee,
                                         'dispositif':dispositif
                                         })
                        print(f"[{count}] OK : {file}")
                        count_ok += 1
                        count += 1
                    elif status == "Non article ciblé":
                        print(f"⛔ Non article ciblé : {file}")
                        count_non_article_ciblé += 1
                    elif status == "Article ciblé sans exposé":
                        print(f"⚠️ Article ciblé mais pas d'exposé : {file}")
                        count_cible_mais_sans_expose += 1
                    else:
                        print(f"❌ Erreur dans {file} : {status}")
                        count_erreur += 1
        print(f"\nNombre total d'amendements article {target_article} avec exposé : {count}")
        print(f"Nombre amendements dans l'article {target_article} mais sans exposé sommaire: {count_cible_mais_sans_expose}")
        print(f"Nombre amendements pas dans l'article {target_article} : {count_non_article_ciblé}")
        print(f"Nombre erreurs: {count_erreur}")

        print("total",count+count_cible_mais_sans_expose+count_non_article_ciblé+count_erreur)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extraction des exposés sommaires d’un article donné.")
    parser.add_argument("input_folder", help="Chemin du dossier contenant les fichiers JSON")
    parser.add_argument("output_csv", help="Chemin du fichier CSV de sortie")
    parser.add_argument("article", type=int, help="Numéro de l'article à filtrer")
    args = parser.parse_args()

    process_folder(args.input_folder, args.output_csv, args.article)
    print(f"Le fichier CSV a été généré avec succès : {args.output_csv}")