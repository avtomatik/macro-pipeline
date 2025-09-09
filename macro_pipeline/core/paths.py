from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_RAW_DIR = BASE_DIR / "data" / "raw"
DATA_OUT_DIR = BASE_DIR / "data" / "processed"

FILE_NAME = "usa_macro_1950_2015.csv"
