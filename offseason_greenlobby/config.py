from pathlib import Path

# Paths
PROJ_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJ_ROOT / "data"
AMENDEMENTS_DIR = DATA_DIR / "processed/amendements.csv"

COL_IDEES = "IDEES"
COL_DESCRIPTION = "DESCRIPTION"
COL_NOM_AMENDEMENT = "NOM_AMENDEMENT"
COL_EXPOSE_SOMMAIRE = "EXPOSE_SOMMAIRE"
COL_LABEL = "LABEL"
COL_PREDICTIONS = "prediction"

METRICS = ["accuracy", "precision", "recall","f1_score"]

color_17 = {
    "Rassemblement National": {
        "groupe_politique_nom": "Rassemblement National",
        "couleur": "#08306b"  # Bleu marine
    },
    "Démocrate (MoDem et Indépendants)": {
        "groupe_politique_nom": "Démocrate (MoDem et Indépendants)",
        "couleur": "#fdbb84"  # Orange clair
    },
    "Renaissance": {
        "groupe_politique_nom": "Renaissance",
        "couleur": "#fdbb84"  # Orange clair
    },
    "Les Républicains": {
        "groupe_politique_nom": "Les Républicains",
        "couleur": "#1e5a85"  # Bleu
    },
    "Libertés, Indépendants, Outre-mer et Territoires": {
        "groupe_politique_nom": "Libertés, Indépendants, Outre-mer et Territoires",
        "couleur": "#bdd7e7"  # Bleu clair
    },
    "Horizons et apparentés": {
        "groupe_politique_nom": "Horizons et apparentés",
        "couleur": "#fdae6b"  # Orange
    },
    "La France insoumise - Nouvelle Union Populaire écologique et sociale": {
        "groupe_politique_nom": "La France insoumise - Nouvelle Union Populaire écologique et sociale",
        "couleur": "#b2182b"  # Rouge foncé
    },
    "Écologiste - NUPES": {
        "groupe_politique_nom": "Écologiste - NUPES",
        "couleur": "#33a02c"  # Vert
    },
    "Socialistes et apparentés": {
        "groupe_politique_nom": "Socialistes et apparentés",
        "couleur": "#fc9272"  # Rose clair
    },
    "Gauche démocrate et républicaine - NUPES": {
        "groupe_politique_nom": "Gauche démocrate et républicaine - NUPES",
        "couleur": "#ef3b2c"  # Rouge
    },
    "Inconnu": {
        "groupe_politique_nom": "Inconnu",
        "couleur": "#cccccc"  # Gris
    },
    "Non inscrit": {
        "groupe_politique_nom": "Non inscrit",
        "couleur": "#999999"  # Gris foncé
    }
}



color_15 = {
    "Les Républicains": {
        "groupe_politique_nom": "Les Républicains",
        "couleur": "#1e5a85"  # Bleu
    },
    "Socialistes et apparentés": {
        "groupe_politique_nom": "Socialistes et apparentés",
        "couleur": "#fc9272"  # Rose clair
    },
    "La République en Marche": {
        "groupe_politique_nom": "La République en Marche",
        "couleur": "#fdbb84"  # Orange clair
    },
    "La France insoumise": {
        "groupe_politique_nom": "La France insoumise",
        "couleur": "#b2182b"  # Rouge foncé
    },
    "Libertés et Territoires": {
        "groupe_politique_nom": "Libertés et Territoires",
        "couleur": "#bdd7e7"  # Bleu clair
    },
    "UDI et Indépendants": {
        "groupe_politique_nom": "UDI et Indépendants",
        "couleur": "#9e9ac8"  # Violet
    },
    "Écologie Démocratie Solidarité": {
        "groupe_politique_nom": "Écologie Démocratie Solidarité",
        "couleur": "#33a02c"  # Vert
    },
    "Mouvement Démocrate (MoDem) et Démocrates apparentés": {
        "groupe_politique_nom": "Mouvement Démocrate (MoDem) et Démocrates apparentés",
        "couleur": "#fee391"  # Jaune clair
    },
    "Inconnu": {
        "groupe_politique_nom": "Inconnu",
        "couleur": "#cccccc"  # Gris
    },
    "Gauche démocrate et républicaine": {
        "groupe_politique_nom": "Gauche démocrate et républicaine",
        "couleur": "#ef3b2c"  # Rouge
    },
    "Agir ensemble": {
        "groupe_politique_nom": "Agir ensemble",
        "couleur": "#fdae6b"  # Orange
    },
    "Non inscrit": {
        "groupe_politique_nom": "Non inscrit",
        "couleur": "#999999"  # Gris foncé
    }
}


color_16 = {
    "Rassemblement National": {
        "groupe_politique_nom": "Rassemblement National",
        "couleur": "#08306b"  # Bleu marine
    },
    "Démocrate (MoDem et Indépendants)": {
        "groupe_politique_nom": "Démocrate (MoDem et Indépendants)",
        "couleur": "#fdbb84"  # Orange clair
    },
    "Renaissance": {
        "groupe_politique_nom": "Renaissance",
        "couleur": "#fdbb84"  # Orange clair
    },
    "Les Républicains": {
        "groupe_politique_nom": "Les Républicains",
        "couleur": "#1e5a85"  # Bleu
    },
    "Libertés, Indépendants, Outre-mer et Territoires": {
        "groupe_politique_nom": "Libertés, Indépendants, Outre-mer et Territoires",
        "couleur": "#bdd7e7"  # Bleu clair
    },
    "Horizons et apparentés": {
        "groupe_politique_nom": "Horizons et apparentés",
        "couleur": "#fdae6b"  # Orange
    },
    "La France insoumise - Nouvelle Union Populaire écologique et sociale": {
        "groupe_politique_nom": "La France insoumise - Nouvelle Union Populaire écologique et sociale",
        "couleur": "#b2182b"  # Rouge foncé
    },
    "Écologiste - NUPES": {
        "groupe_politique_nom": "Écologiste - NUPES",
        "couleur": "#33a02c"  # Vert
    },
    "Socialistes et apparentés": {
        "groupe_politique_nom": "Socialistes et apparentés",
        "couleur": "#fc9272"  # Rose clair
    },
    "Gauche démocrate et républicaine - NUPES": {
        "groupe_politique_nom": "Gauche démocrate et républicaine - NUPES",
        "couleur": "#ef3b2c"  # Rouge
    },
    "Inconnu": {
        "groupe_politique_nom": "Inconnu",
        "couleur": "#cccccc"  # Gris
    },
    "Non inscrit": {
        "groupe_politique_nom": "Non inscrit",
        "couleur": "#999999"  # Gris foncé
    }
}



gp_agec_senat = {
    "Union Centriste": {
        "groupe_politique_nom": "Union Centriste",
        "couleur": "#66c2a5"  # Vert-bleu
    },
    "Les Républicains": {
        "groupe_politique_nom": "Les Républicains",
        "couleur": "#1e5a85"  # Bleu
    },
    "Les Indépendants - République et Territoires": {
        "groupe_politique_nom": "Les Indépendants - République et Territoires",
        "couleur": "#fdae6b"  # Orange
    },
    "Socialiste, Écologiste et Républicain": {
        "groupe_politique_nom": "Socialiste, Écologiste et Républicain",
        "couleur": "#fc9272"  # Rose clair
    },
    "Rassemblement des démocrates, progressistes et indépendants": {
        "groupe_politique_nom": "Rassemblement des démocrates, progressistes et indépendants",
        "couleur": "#fee391"  # Jaune clair
    },
    "Écologiste - Solidarité et Territoires": {
        "groupe_politique_nom": "Écologiste - Solidarité et Territoires",
        "couleur": "#33a02c"  # Vert
    },
    "du Rassemblement Démocratique et Social Européen": {
        "groupe_politique_nom": "Rassemblement Démocratique et Social Européen",
        "couleur": "#fdbb84"  # Orange clair
    },
    "socialiste et républicain": {
        "groupe_politique_nom": "Socialiste et Républicain",
        "couleur": "#fc9272"  # Rose clair
    },
    "Inconnu": {
        "groupe_politique_nom": "Inconnu",
        "couleur": "#cccccc"  # Gris
    },
    "Communiste Républicain Citoyen et Écologiste - Kanaky": {
        "groupe_politique_nom": "Communiste Républicain Citoyen et Écologiste - Kanaky",
        "couleur": "#b2182b"  # Rouge foncé
    }
}


gp_lv_senat = {
    "Écologiste - Solidarité et Territoires": {
        "groupe_politique_nom": "Écologiste - Solidarité et Territoires",
        "couleur": "#33a02c"  # Vert
    },
    "Les Républicains": {
        "groupe_politique_nom": "Les Républicains",
        "couleur": "#1e5a85"  # Bleu
    },
    "Union Centriste": {
        "groupe_politique_nom": "Union Centriste",
        "couleur": "#66c2a5"  # Vert-bleu
    },
    "Rassemblement des démocrates, progressistes et indépendants": {
        "groupe_politique_nom": "Rassemblement des démocrates, progressistes et indépendants",
        "couleur": "#fee391"  # Jaune clair
    },
    "Socialiste, Écologiste et Républicain": {
        "groupe_politique_nom": "Socialiste, Écologiste et Républicain",
        "couleur": "#fc9272"  # Rose clair
    },
    "Les Indépendants - République et Territoires": {
        "groupe_politique_nom": "Les Indépendants - République et Territoires",
        "couleur": "#fdae6b"  # Orange
    },
    "Rassemblement Démocratique et Social Européen": {
        "groupe_politique_nom": "Rassemblement Démocratique et Social Européen",
        "couleur": "#fdbb84"  # Orange clair
    },
    "Communiste Républicain Citoyen et Écologiste - Kanaky": {
        "groupe_politique_nom": "Communiste Républicain Citoyen et Écologiste - Kanaky",
        "couleur": "#b2182b"  # Rouge foncé
    },
    "Inconnu": {
        "groupe_politique_nom": "Inconnu",
        "couleur": "#cccccc"  # Gris
    }
}


gp_loa_senat = {
    "Les Républicains": {
        "groupe_politique_nom": "Les Républicains",
        "couleur": "#1e5a85"  # Bleu
    },
    "Union Centriste": {
        "groupe_politique_nom": "Union Centriste",
        "couleur": "#66c2a5"  # Vert-bleu
    },
    "Les Indépendants - République et Territoires": {
        "groupe_politique_nom": "Les Indépendants - République et Territoires",
        "couleur": "#fdae6b"  # Orange
    },
    "Socialiste, Écologiste et Républicain": {
        "groupe_politique_nom": "Socialiste, Écologiste et Républicain",
        "couleur": "#fc9272"  # Rose clair
    },
    "Rassemblement des démocrates, progressistes et indépendants": {
        "groupe_politique_nom": "Rassemblement des démocrates, progressistes et indépendants",
        "couleur": "#fee391"  # Jaune clair
    },
    "du Rassemblement Démocratique et Social Européen": {
        "groupe_politique_nom": "Rassemblement Démocratique et Social Européen",
        "couleur": "#fdbb84"  # Orange clair
    },
    "Délégué de la réunion administrative des Sénateurs ne figurant sur la liste d'aucun groupe politique": {
        "groupe_politique_nom": "Non inscrit",
        "couleur": "#999999"  # Gris foncé
    },
    "Membre de la réunion administrative des Sénateurs ne figurant sur la liste d'aucun groupe politique": {
        "groupe_politique_nom": "Non inscrit",
        "couleur": "#999999"  # Gris foncé
    },
    "Écologiste - Solidarité et Territoires": {
        "groupe_politique_nom": "Écologiste - Solidarité et Territoires",
        "couleur": "#33a02c"  # Vert
    },
    "Communiste Républicain Citoyen et Écologiste - Kanaky": {
        "groupe_politique_nom": "Communiste Républicain Citoyen et Écologiste - Kanaky",
        "couleur": "#b2182b"  # Rouge foncé
    },
    "Inconnu": {
        "groupe_politique_nom": "Inconnu",
        "couleur": "#cccccc"  # Gris
    }
}

