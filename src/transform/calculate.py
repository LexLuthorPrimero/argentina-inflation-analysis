import pandas as pd
from src.utils.logging import setup_logger

logger = setup_logger(__name__)

def calcular_variacion_anual(df):
    """
    Calcula la variación porcentual interanual de la inflación.
    df: DataFrame con columnas 'year' e 'inflacion_anual'
    """
    df = df.copy()
    df['variacion'] = df['inflacion_anual'].pct_change() * 100
    return df