from pathlib import Path

# Paths
PROJ_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJ_ROOT / "data"
AMENDEMENTS_DIR = DATA_DIR / "processed/amendements.csv"

COL_IDEES = "IDEES"
COL_DESCRIPTION = "DESCRIPTION"
COL_NOM_AMENDEMENT = "NOM_AMENDEMENT"

COL_LABEL = "LABEL"
COL_PREDICTIONS = "prediction"

METRICS = ["accuracy", "precision", "recall","f1_score"]
