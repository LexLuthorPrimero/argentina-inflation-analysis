import requests
import pandas as pd
from src.utils.logging import setup_logger

logger = setup_logger(__name__)

def extract_inflation_worldbank(country="AR", start=2000, end=2025):
    logger.info(f"Extrayendo datos del Banco Mundial para {country} ({start}-{end})")
    url = f"http://api.worldbank.org/v2/country/{country}/indicator/FP.CPI.TOTL.ZG"
    params = {"format": "json", "per_page": 100, "date": f"{start}:{end}"}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        records = data[1] if len(data) > 1 else []
        rows = []
        for item in records:
            if item["value"] is not None:
                rows.append({"year": int(item["date"]), "inflacion_anual": float(item["value"])})
        df = pd.DataFrame(rows)
        logger.info(f"Descargadas {len(df)} filas")
        return df
    except Exception as e:
        logger.error(f"Error: {e}")
        return None