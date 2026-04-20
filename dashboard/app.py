import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Configurar la página
st.set_page_config(page_title="Inflación Argentina", layout="wide")
st.title("📈 Análisis de Inflación en Argentina")
st.markdown("Datos extraídos del Banco Mundial (inflación anual)")

# Cargar datos
@st.cache_data
def load_data():
    # Datos crudos
    raw_path = Path("data/raw/worldbank_inflation.csv")
    if raw_path.exists():
        df_raw = pd.read_csv(raw_path)
        df_raw['year'] = df_raw['year'].astype(int)
    else:
        df_raw = None
    
    # Datos procesados (indicadores)
    proc_path = Path("data/processed/worldbank_indicators.csv")
    if proc_path.exists():
        df_proc = pd.read_csv(proc_path)
        df_proc['year'] = df_proc['year'].astype(int)
    else:
        df_proc = None
    
    return df_raw, df_proc

df_raw, df_proc = load_data()

if df_raw is not None:
    # Mostrar tabla de datos
    st.subheader("📊 Datos históricos")
    st.dataframe(df_raw, use_container_width=True)
    
    # Gráfico de líneas
    st.subheader("📉 Evolución de la inflación anual")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df_raw['year'], df_raw['inflacion_anual'], marker='o', linestyle='-', color='#d62728')
    ax.set_xlabel("Año")
    ax.set_ylabel("Inflación anual (%)")
    ax.set_title("Inflación anual en Argentina (fuente: Banco Mundial)")
    ax.grid(True, linestyle='--', alpha=0.7)
    st.pyplot(fig)
    
    # Métricas destacadas
    if df_proc is not None:
        st.subheader("📌 Indicadores clave")
        ultimo = df_proc.iloc[-1]
        col1, col2, col3 = st.columns(3)
        col1.metric("Último año", int(ultimo['year']), delta=None)
        col2.metric("Inflación anual (%)", f"{ultimo['inflacion_anual']:.1f}%")
        col3.metric("Promedio histórico (%)", f"{df_proc['inflacion_anual'].mean():.1f}%")
        
        # Tabla de últimos 5 años
        st.subheader("🔍 Últimos 5 años")
        st.dataframe(df_proc.tail(5), use_container_width=True)
        
        # Gráfico de barras para los últimos 5 años
        st.subheader("📊 Últimos 5 años")
        fig2, ax2 = plt.subplots(figsize=(10, 5))
        ultimos5 = df_proc.tail(5)
        ax2.bar(ultimos5['year'].astype(str), ultimos5['inflacion_anual'], color='#ff7f0e')
        ax2.set_xlabel("Año")
        ax2.set_ylabel("Inflación anual (%)")
        ax2.set_title("Inflación últimos 5 años")
        st.pyplot(fig2)
else:
    st.error("No se encontraron datos. Ejecutá primero 'python scripts/run_etl.py' y luego 'python scripts/run_analysis.py'")

st.markdown("---")
st.caption("Datos del Banco Mundial - Proyecto de análisis de inflación Argentina")