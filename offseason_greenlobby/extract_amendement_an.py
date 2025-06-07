import os
import json
import csv
import html
import re
import argparse
from utils.utils import get_gp,get_gp_nom,get_id_nom,get_id_prenom
from pathlib import Path




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

def extract_expose_sommaire(json_path):
    """Extrait le texte du champ 'exposeSommaire' d'un fichier JSON et identifie la raison s’il n’est pas retenu."""
    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            article_courte = data.get('amendement', {}).get('pointeurFragmentTexte', {}).get('division', {}).get('articleDesignationCourte', '')
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

def process_folder(input_folder, output_csv, folder_acteurs):
    with open(output_csv, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
                'nom_du_fichier', 
                'expose_sommaire',
                'dispositif',
                'article_courte',
                'article',
                'type_amendement',
                'groupe_politique_ref',
                'groupe_politique',
                'groupe_politique_nom',
                'type_auteur',
                'acteur_ref',
                'acteur_nom',
                'acteur_prenom',
                'acteur_denom'
                ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        count_ok = 0
        count_non_article_ciblé = 0
        count_cible_mais_sans_expose = 0
        count_erreur = 0

        count = 0
        # Replace this with the path to your top-level folder
        base_folder = Path(input_folder)
        all_files = [f for f in base_folder.rglob('*.json') if f.is_file()]
        
        for json_path in all_files:
            expose_sommaire, status, typeAuteur , acteurRef, groupePolitiqueRef, article_courte, typee,dispositif = extract_expose_sommaire(json_path)
            file = str(json_path).split('/')[-1]
            if status == "OK":
                if folder_acteurs:
                    acteurs = folder_acteurs + "/acteurs/"
                    organes = folder_acteurs + "/organes/"
                    acteur_nom = get_id_nom(acteurs,acteurRef) if len(acteurRef) == 8 else "Inconnu"
                    acteur_prenom = get_id_prenom(acteurs,acteurRef) if len(acteurRef) == 8 else "Inconnu"
                    acteur_denom = acteur_nom + ' ' + acteur_prenom
                    writer.writerow({
                                'nom_du_fichier':file, 
                                'expose_sommaire':expose_sommaire,
                                'dispositif':dispositif,
                                'article_courte':article_courte,
                                'article':re.findall(r'\d+', article_courte)[0] if len(re.findall(r'\d+', article_courte))> 0 else "1",
                                'type_amendement':typee,
                                'groupe_politique_ref':groupePolitiqueRef,
                                'groupe_politique':get_gp(organes,groupePolitiqueRef) if len(groupePolitiqueRef) == 8 else "Inconnu",
                                'groupe_politique_nom':get_gp_nom(organes,groupePolitiqueRef) if len(groupePolitiqueRef) == 8 else "Inconnu",
                                'type_auteur':typeAuteur,
                                'acteur_ref':acteurRef,
                                'acteur_nom':acteur_nom,
                                'acteur_prenom':acteur_prenom,
                                'acteur_denom': acteur_denom

                                    })
                    print(f"[{count}] OK : {file}")
                    count_ok += 1
                    count += 1
                else:
                    writer.writerow({
                                'nom_du_fichier':file, 
                                'expose_sommaire':expose_sommaire,
                                'dispositif':dispositif,
                                'article_courte':article_courte,
                                'type_amendement':typee,
                                'groupe_politique_ref':groupePolitiqueRef,
                                'type_auteur':typeAuteur,
                                    })
                    print(f"[{count}] OK : {file}")
                    count_ok += 1
                    count += 1
            else:
                print(f"❌ Erreur dans {file} : {status}")
                count_erreur += 1
        print(f"Nombre amendements mais sans exposé sommaire: {count_cible_mais_sans_expose}")
        print(f"Nombre erreurs: {count_erreur}")

        print("total",count+count_cible_mais_sans_expose+count_erreur)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extraction des exposés sommaires d’un projet de Loi.")
    parser.add_argument("--input_folder", help="Chemin du dossier contenant les fichiers JSON")
    parser.add_argument("--output_csv", help="Chemin du fichier CSV de sortie")
    parser.add_argument("--folder_acteurs", help="Chemin du dossier contenant données des députés/groupes parlementaires de la legislature")
    args = parser.parse_args()

    process_folder(args.input_folder, args.output_csv, args.folder_acteurs)
    print(f"Le fichier CSV a été généré avec succès : {args.output_csv}")