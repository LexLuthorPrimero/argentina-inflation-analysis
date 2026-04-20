#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.extract.worldbank import extract_inflation_worldbank
from src.utils.logging import setup_logger

logger = setup_logger("etl")

def main():
    logger.info("Iniciando ETL")
    df = extract_inflation_worldbank()
    if df is not None:
        df.to_csv("data/raw/worldbank_inflation.csv", index=False)
        logger.info("Guardado en data/raw/worldbank_inflation.csv")
    else:
        logger.error("Fallo la extracción")

if __name__ == "__main__":
    main()