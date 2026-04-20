import requests
import pandas as pd
from src.utils.logging import setup_logger

logger = setup_logger(__name__)

def extract_inflation_bcra(start_year=2017):
    """
    Extrae inflación mensual del BCRA (IPC Nivel General - Base 2016=100)
    Fuente: API de estadísticas del BCRA (variable 'IPCNG')
    """
    # ID de la variable: IPC Nivel General (variación porcentual mensual)
    # Se puede obtener del catálogo: https://www.bcra.gob.ar/Catalogo_de_datos/principales-variables.aspx
    variable_id = "IPCNG"  # Por defecto; si no funciona, usaremos otra fuente
    
    url = f"https://api.bcra.gob.ar/estadisticas/v2.0/datosvariable/{variable_id}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get('status') == 200:
            registros = data.get('results', [])
            df = pd.DataFrame(registros)
            if not df.empty:
                df.rename(columns={'fecha': 'date', 'valor': 'inflacion_mensual'}, inplace=True)
                df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
                df = df[df['date'].dt.year >= start_year]
                logger.info(f"Descargadas {len(df)} filas mensuales del BCRA")
                return df
        else:
            logger.error(f"Error API BCRA: {data.get('message')}")
            return None
    except Exception as e:
        logger.error(f"Error al extraer del BCRA: {e}")
        return None

if __name__ == "__main__":
    df = extract_inflation_bcra()
    if df is not None:
        print(df.tail())