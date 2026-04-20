import os
from dotenv import load_dotenv

load_dotenv()

def get_bcra_token():
    return os.getenv("BCRA_API_TOKEN")

DATA_RAW_PATH = "data/raw"
DATA_PROCESSED_PATH = "data/processed"
DATABASE_PATH = "data/database/inflation.db"