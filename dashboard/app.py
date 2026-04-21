import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Configuración de la página
st.set_page_config(page_title="Inflación Argentina - Dashboard Interactivo", layout="wide")
st.title("📈 Análisis Interactivo de Inflación en Argentina")

# Cargar datos
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

if df_raw is None:
    st.error("No se encontraron datos. Ejecuta primero 'python scripts/run_etl.py'")
    st.stop()

# ==================== INTERACTIVIDAD ====================

st.sidebar.header("🔍 Filtros interactivos")

# 1. Selector de rango de años
min_year = int(df_raw['year'].min())
max_year = int(df_raw['year'].max())
year_range = st.sidebar.slider(
    "Seleccionar rango de años",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

# 2. Tipo de gráfico
chart_type = st.sidebar.selectbox(
    "Tipo de gráfico",
    options=["Línea", "Barras", "Ambos"]
)

# 3. Mostrar tabla de datos?
show_table = st.sidebar.checkbox("Mostrar tabla de datos", value=True)

# 4. Mostrar indicadores clave?
show_metrics = st.sidebar.checkbox("Mostrar indicadores clave", value=True)

# Filtrar datos según rango de años
df_filtered = df_raw[(df_raw['year'] >= year_range[0]) & (df_raw['year'] <= year_range[1])]

# Mostrar métricas
if show_metrics and df_proc is not None:
    st.subheader("📊 Indicadores clave (en el rango seleccionado)")
    # Filtrar métricas según rango
    df_proc_filtered = df_proc[(df_proc['year'] >= year_range[0]) & (df_proc['year'] <= year_range[1])]
    if not df_proc_filtered.empty:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Último año", int(df_proc_filtered['year'].iloc[-1]))
        col2.metric("Inflación anual (%)", f"{df_proc_filtered['inflacion_anual'].iloc[-1]:.1f}%")
        col3.metric("Máximo histórico", f"{df_proc_filtered['inflacion_anual'].max():.1f}%")
        col4.metric("Promedio", f"{df_proc_filtered['inflacion_anual'].mean():.1f}%")
    else:
        st.info("No hay datos en el rango seleccionado")

# Gráficos interactivos
st.subheader(f"Evolución de la inflación ({year_range[0]} - {year_range[1]})")

fig, ax = plt.subplots(figsize=(10, 5))

if chart_type in ["Línea", "Ambos"]:
    ax.plot(df_filtered['year'], df_filtered['inflacion_anual'], marker='o', linestyle='-', color='#d62728', label='Inflación anual')
if chart_type in ["Barras", "Ambos"]:
    ax.bar(df_filtered['year'], df_filtered['inflacion_anual'], alpha=0.5, color='#ff7f0e', label='Inflación anual (barras)')

ax.set_xlabel("Año")
ax.set_ylabel("Inflación anual (%)")
ax.set_title(f"Evolución de la inflación en Argentina ({year_range[0]}-{year_range[1]})")
ax.grid(True, linestyle='--', alpha=0.7)
ax.legend()
st.pyplot(fig)

# Tabla de datos
if show_table:
    st.subheader("📋 Datos históricos (rango seleccionado)")
    st.dataframe(df_filtered, use_container_width=True)

# Opcional: descargar datos filtrados
csv = df_filtered.to_csv(index=False)
st.download_button(
    label="📥 Descargar datos filtrados (CSV)",
    data=csv,
    file_name=f"inflacion_argentina_{year_range[0]}_{year_range[1]}.csv",
    mime="text/csv"
)

st.caption("Fuente: Banco Mundial (indicador FP.CPI.TOTL.ZG) - Dashboard interactivo con Streamlit")