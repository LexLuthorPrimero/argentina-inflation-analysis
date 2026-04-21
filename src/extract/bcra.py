import requests
import pandas as pd
from src.utils.logging import setup_logger
from src.utils.config import get_bcra_token

logger = setup_logger(__name__)


def extract_inflation_bcra(start_year: int = 2017) -> pd.DataFrame | None:
    """
    Extrae inflación mensual del BCRA a través de la API de estadisticasbcra.com.
    Requiere token en .env (BCRA_API_TOKEN)
    """
    token = get_bcra_token()
    if not token:
        logger.error(
            "No se encontró el token del BCRA. Configurar BCRA_API_TOKEN en .env"
        )
        return None

    url = "https://api.estadisticasbcra.com/inflacion_mensual_oficial"
    headers = {"Authorization": f"BEARER {token}"}

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()

        if data:
            rows = [
                {"date": item["d"], "inflacion_mensual": item["v"]} for item in data
            ]
            df = pd.DataFrame(rows)
            df["date"] = pd.to_datetime(df["date"])
            df = df[df["date"].dt.year >= start_year]
            df = df.sort_values("date")
            logger.info(
                f"Descargadas {len(df)} filas de inflación mensual desde estadisticasbcra.com."
            )
            return df
        else:
            logger.warning("No se encontraron datos en la respuesta.")
            return None
    except Exception as e:
        logger.error(f"Error al extraer datos de estadisticasbcra.com: {e}")
        return None


if __name__ == "__main__":
    df = extract_inflation_bcra()
    if df is not None:
        print(df.tail())
