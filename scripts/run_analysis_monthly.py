#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import matplotlib.pyplot as plt
from src.utils.logging import setup_logger

logger = setup_logger("analisis_mensual")


def main():
    df = pd.read_csv("data/raw/bcra_inflation_monthly.csv")
    df["date"] = pd.to_datetime(df["date"])
    logger.info(f"Cargados {len(df)} registros mensuales")

    # Calcular acumulado anual
    df["year"] = df["date"].dt.year
    anual = df.groupby("year")["inflacion_mensual"].sum().reset_index()
    anual.to_csv("data/processed/inflacion_mensual_acumulada.csv", index=False)

    # Gráfico mensual
    plt.figure(figsize=(12, 5))
    plt.plot(df["date"], df["inflacion_mensual"], marker=".", alpha=0.7)
    plt.title("Inflación mensual Argentina")
    plt.xlabel("Fecha")
    plt.ylabel("Variación mensual (%)")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.savefig("reports/inflacion_mensual.png")
    logger.info("Gráfico mensual guardado")


if __name__ == "__main__":
    main()
