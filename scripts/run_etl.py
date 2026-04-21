#!/usr/bin/env python3
"""Pipeline ETL principal: extrae datos del Banco Mundial y del BCRA."""
import sys
from pathlib import Path

# Agregar la raíz del proyecto al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.extract.worldbank import extract_inflation_worldbank
from src.extract.bcra import extract_inflation_bcra
from src.utils.logging import setup_logger

logger = setup_logger("etl")

def main():
    logger.info("Iniciando pipeline ETL de inflación Argentina")
    
    # 1. Extraer datos del Banco Mundial (anuales)
    df_wb = extract_inflation_worldbank()
    if df_wb is not None:
        df_wb.to_csv("data/raw/worldbank_inflation.csv", index=False)
        logger.info("Datos anuales del Banco Mundial guardados en data/raw/worldbank_inflation.csv")
    else:
        logger.error("Fallo la extracción de datos del Banco Mundial")
    
    # 2. Extraer datos del BCRA (mensuales)
    df_bcra = extract_inflation_bcra()
    if df_bcra is not None:
        df_bcra.to_csv("data/raw/bcra_inflation_monthly.csv", index=False)
        logger.info("Datos mensuales del BCRA guardados en data/raw/bcra_inflation_monthly.csv")
    else:
        logger.warning("No se pudieron obtener datos del BCRA")
    
    logger.info("Pipeline ETL finalizado")

if __name__ == "__main__":
    main()