import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(page_title="Inflación Argentina", layout="wide")
st.title("📈 Análisis de Inflación en Argentina")

@st.cache_data
def load_data():
    raw_path = Path("data/raw/worldbank_inflation.csv")
    if raw_path.exists():
        df_raw = pd.read_csv(raw_path)
        df_raw['year'] = df_raw['year'].astype(int)
    else:
        df_raw = None
    proc_path = Path("data/processed/worldbank_indicators.csv")
    if proc_path.exists():
        df_proc = pd.read_csv(proc_path)
        df_proc['year'] = df_proc['year'].astype(int)
    else:
        df_proc = None
    return df_raw, df_proc

df_raw, df_proc = load_data()
if df_raw is not None:
    st.subheader("📊 Datos históricos")
    st.dataframe(df_raw, use_container_width=True)
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(df_raw['year'], df_raw['inflacion_anual'], marker='o', color='#d62728')
    ax.set_xlabel("Año")
    ax.set_ylabel("Inflación anual (%)")
    ax.grid(True, linestyle='--', alpha=0.7)
    st.pyplot(fig)
    if df_proc is not None:
        st.subheader("📌 Indicadores clave")
        ultimo = df_proc.iloc[-1]
        col1, col2, col3 = st.columns(3)
        col1.metric("Último año", int(ultimo['year']))
        col2.metric("Inflación anual (%)", f"{ultimo['inflacion_anual']:.1f}%")
        col3.metric("Promedio histórico (%)", f"{df_proc['inflacion_anual'].mean():.1f}%")
else:
    st.error("No se encontraron datos. Ejecuta primero 'python scripts/run_etl.py'")