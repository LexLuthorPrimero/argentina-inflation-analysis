#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import matplotlib.pyplot as plt
from src.transform.calculate import calcular_variacion_anual
from src.utils.logging import setup_logger

logger = setup_logger("analisis")

def main():
    # Cargar datos anuales
    df = pd.read_csv("data/raw/worldbank_inflation.csv")
    logger.info(f"Datos cargados: {len(df)} registros")
    
    # Calcular variación interanual
    df = calcular_variacion_anual(df)
    
    # Guardar indicadores procesados
    df.to_csv("data/processed/worldbank_indicators.csv", index=False)
    logger.info("Datos procesados guardados en data/processed/worldbank_indicators.csv")
    
    # Generar gráfico
    plt.figure(figsize=(10,5))
    plt.plot(df['year'], df['inflacion_anual'], marker='o', linestyle='-', color='#d62728')
    plt.title("Inflación anual Argentina")
    plt.xlabel("Año")
    plt.ylabel("Inflación anual (%)")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig("reports/inflacion_anual_argentina.png")
    logger.info("Gráfico guardado en reports/inflacion_anual_argentina.png")
    
    # Mostrar resumen
    print("\n=== RESUMEN DE INDICADORES ===\n")
    ultimo = df.iloc[-1]
    print(f"Último año disponible: {ultimo['year']}")
    print(f"Última inflación anual: {ultimo['inflacion_anual']:.2f}%")
    print(f"Máximo histórico: {df['inflacion_anual'].max():.2f}%")
    print(f"Promedio histórico: {df['inflacion_anual'].mean():.2f}%\n")
    print("Últimos 5 años:")
    print(df.tail(5).to_string(index=False))

if __name__ == "__main__":
    main()