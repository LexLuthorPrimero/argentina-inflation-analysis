#!/usr/bin/env python3
"""Genera indicadores y gráficos a partir de los datos extraídos"""
import sys
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.transform.calculate import calcular_indicadores_anuales
from src.utils.logging import setup_logger

logger = setup_logger("analisis")

def main():
    # 1. Cargar datos crudos
    raw_path = Path("data/raw/worldbank_inflation.csv")
    if not raw_path.exists():
        logger.error(f"No se encuentra {raw_path}. Ejecutá primero run_etl.py")
        return
    
    df_raw = pd.read_csv(raw_path)
    logger.info(f"Datos cargados: {len(df_raw)} registros")
    
    # 2. Calcular indicadores
    df = calcular_indicadores_anuales(df_raw)
    if df is None:
        return
    
    # 3. Guardar datos procesados
    processed_path = Path("data/processed/worldbank_indicators.csv")
    processed_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(processed_path, index=False)
    logger.info(f"Datos procesados guardados en {processed_path}")
    
    # 4. Generar gráfico
    plt.style.use('seaborn-v0_8-darkgrid')
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Línea principal
    ax.plot(df['year'], df['inflacion_anual'], marker='o', linewidth=2, label='Inflación anual %')
    
    # Promedio móvil
    ax.plot(df['year'], df['promedio_movil_3'], '--', linewidth=1.5, label='Promedio móvil 3 años')
    
    # Personalización
    ax.set_title('Evolución de la Inflación Anual en Argentina (fuente: Banco Mundial)', fontsize=14)
    ax.set_xlabel('Año')
    ax.set_ylabel('Inflación (%)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Rotar etiquetas si muchos años
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Guardar gráfico
    report_dir = Path("reports")
    report_dir.mkdir(exist_ok=True)
    plt.savefig(report_dir / "inflacion_anual_argentina.png", dpi=150)
    logger.info(f"Gráfico guardado en {report_dir / 'inflacion_anual_argentina.png'}")
    
    # Mostrar resumen en consola
    print("\n=== RESUMEN DE INDICADORES ===\n")
    print(f"Último año disponible: {df['year'].iloc[-1]}")
    print(f"Última inflación anual: {df['inflacion_anual'].iloc[-1]:.2f}%")
    print(f"Máximo histórico: {df['maximo_historico'].max():.2f}%")
    print(f"Promedio histórico: {df['inflacion_anual'].mean():.2f}%")
    
    # Mostrar últimos 5 años
    print("\nÚltimos 5 años:")
    print(df[['year', 'inflacion_anual', 'variacion_respecto_anio_anterior']].tail(5).to_string(index=False))

if __name__ == "__main__":
    main()