"""Cálculos de indicadores de inflación a partir de datos anuales del Banco Mundial"""
import pandas as pd
from src.utils.logging import setup_logger

logger = setup_logger(__name__)

def calcular_indicadores_anuales(df):
    """
    Calcula indicadores adicionales sobre datos anuales de inflación.
    df debe tener columnas: year, inflacion_anual
    """
    if df is None or df.empty:
        logger.error("DataFrame vacío o nulo")
        return None
    
    df = df.copy()
    df = df.sort_values('year')
    
    # Inflación acumulada (no aplica para anual, pero calculamos variación respecto al año anterior)
    df['variacion_respecto_anio_anterior'] = df['inflacion_anual'].pct_change() * 100
    
    # Promedio móvil de 3 años
    df['promedio_movil_3'] = df['inflacion_anual'].rolling(window=3).mean()
    
    # Máximo histórico hasta el momento
    df['maximo_historico'] = df['inflacion_anual'].cummax()
    
    logger.info(f"Indicadores calculados para {len(df)} años")
    return df

if __name__ == "__main__":
    # Prueba rápida con datos de ejemplo
    test_data = pd.DataFrame({
        'year': [2000, 2001, 2002],
        'inflacion_anual': [10.0, 12.0, 15.0]
    })
    result = calcular_indicadores_anuales(test_data)
    print(result)