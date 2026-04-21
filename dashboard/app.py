import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Configuración de la página
st.set_page_config(page_title="Inflación Argentina", layout="wide")
st.title("📊 Inflación Argentina - Dashboard Interactivo")

# Funciones de carga de datos (con caché)
@st.cache_data
def load_annual_data():
    path = Path("data/raw/worldbank_inflation.csv")
    if path.exists():
        df = pd.read_csv(path)
        df['year'] = df['year'].astype(int)
        return df
    return None

@st.cache_data
def load_monthly_data():
    path = Path("data/raw/bcra_inflation_monthly.csv")
    if path.exists():
        df = pd.read_csv(path)
        df['date'] = pd.to_datetime(df['date'])
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        return df
    return None

@st.cache_data
def load_annual_indicators():
    path = Path("data/processed/worldbank_indicators.csv")
    if path.exists():
        df = pd.read_csv(path)
        df['year'] = df['year'].astype(int)
        return df
    return None

# Cargar datos
df_anual = load_annual_data()
df_mensual = load_monthly_data()
df_indicadores = load_annual_indicators()

if df_anual is None:
    st.error("No se encontraron datos anuales. Ejecuta primero 'python scripts/run_etl.py'")
    st.stop()

# ==================== BARRA LATERAL ====================
st.sidebar.header("⚙️ Configuración")
tema = st.sidebar.selectbox("Tema de gráficos", ["default", "oscuro"])
if tema == "oscuro":
    plt.style.use('dark_background')

# ==================== TABS ====================
tab1, tab2, tab3 = st.tabs(["📈 Inflación Anual (World Bank)", "📉 Inflación Mensual (BCRA)", "📊 Comparación"])

# ---------- TAB 1: Anual ----------
with tab1:
    st.subheader("Evolución anual de la inflación")
    
    # Filtro de rango de años
    min_year = int(df_anual['year'].min())
    max_year = int(df_anual['year'].max())
    year_range = st.slider("Seleccionar rango de años", min_year, max_year, (min_year, max_year), key="anual_range")
    
    df_filtrado = df_anual[(df_anual['year'] >= year_range[0]) & (df_anual['year'] <= year_range[1])]
    
    # Tipo de gráfico
    chart_type = st.radio("Tipo de gráfico", ["Línea", "Barras", "Ambos"], horizontal=True, key="anual_chart")
    
    fig, ax = plt.subplots(figsize=(10, 5))
    if chart_type in ["Línea", "Ambos"]:
        ax.plot(df_filtrado['year'], df_filtrado['inflacion_anual'], marker='o', color='#d62728', label='Inflación anual')
    if chart_type in ["Barras", "Ambos"]:
        ax.bar(df_filtrado['year'], df_filtrado['inflacion_anual'], alpha=0.5, color='#ff7f0e', label='Inflación anual')
    ax.set_xlabel("Año")
    ax.set_ylabel("Inflación anual (%)")
    ax.set_title(f"Evolución de la inflación anual ({year_range[0]}-{year_range[1]})")
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend()
    st.pyplot(fig)
    
    # Mostrar tabla
    if st.checkbox("Mostrar tabla", value=True, key="anual_table"):
        st.dataframe(df_filtrado, use_container_width=True)
    
    # Descarga CSV
    csv = df_filtrado.to_csv(index=False)
    st.download_button("📥 Descargar datos anuales (CSV)", csv, "inflacion_anual.csv", "text/csv")

# ---------- TAB 2: Mensual ----------
with tab2:
    if df_mensual is None:
        st.warning("Datos mensuales no disponibles. Ejecuta el pipeline ETL que incluye BCRA.")
    else:
        st.subheader("Inflación mensual (BCRA)")
        
        # Filtro de fechas
        min_date = df_mensual['date'].min().date()
        max_date = df_mensual['date'].max().date()
        date_range = st.slider("Seleccionar rango de fechas", min_date, max_date, (min_date, max_date), format="YYYY-MM", key="mensual_range")
        
        df_mensual_filtrado = df_mensual[(df_mensual['date'].dt.date >= date_range[0]) & (df_mensual['date'].dt.date <= date_range[1])]
        
        # Tipo de gráfico
        chart_type_m = st.radio("Tipo de gráfico", ["Línea", "Barras", "Ambos"], horizontal=True, key="mensual_chart")
        
        fig2, ax2 = plt.subplots(figsize=(12, 5))
        if chart_type_m in ["Línea", "Ambos"]:
            ax2.plot(df_mensual_filtrado['date'], df_mensual_filtrado['inflacion_mensual'], marker='.', color='#1f77b4', label='Inflación mensual')
        if chart_type_m in ["Barras", "Ambos"]:
            ax2.bar(df_mensual_filtrado['date'], df_mensual_filtrado['inflacion_mensual'], width=20, alpha=0.5, color='#2ca02c', label='Inflación mensual')
        ax2.set_xlabel("Fecha")
        ax2.set_ylabel("Variación mensual (%)")
        ax2.set_title("Inflación mensual Argentina")
        ax2.grid(True, linestyle='--', alpha=0.6)
        ax2.legend()
        st.pyplot(fig2)
        
        # Métricas adicionales
        col1, col2, col3 = st.columns(3)
        ultimo_mes = df_mensual_filtrado.iloc[-1]
        col1.metric("Último mes", ultimo_mes['date'].strftime('%Y-%m'), f"{ultimo_mes['inflacion_mensual']:.2f}%")
        max_mensual = df_mensual_filtrado['inflacion_mensual'].max()
        col2.metric("Máximo mensual", f"{max_mensual:.2f}%", delta=None)
        promedio_mensual = df_mensual_filtrado['inflacion_mensual'].mean()
        col3.metric("Promedio mensual", f"{promedio_mensual:.2f}%", delta=None)
        
        # Tabla
        if st.checkbox("Mostrar tabla mensual", value=True, key="mensual_table"):
            st.dataframe(df_mensual_filtrado, use_container_width=True)
        
        # Descarga
        csv_m = df_mensual_filtrado.to_csv(index=False)
        st.download_button("📥 Descargar datos mensuales (CSV)", csv_m, "inflacion_mensual.csv", "text/csv")

# ---------- TAB 3: Comparación anual vs mensual acumulado ----------
with tab3:
    st.subheader("Comparación: Inflación anual (World Bank) vs. Acumulado mensual (BCRA)")
    if df_mensual is not None:
        # Calcular inflación acumulada por año a partir de datos mensuales
        acumulado_anual = df_mensual.groupby('year')['inflacion_mensual'].sum().reset_index()
        acumulado_anual.rename(columns={'inflacion_mensual': 'acumulado_bcra'}, inplace=True)
        
        # Unir con datos anuales del Banco Mundial
        comparativa = df_anual.merge(acumulado_anual, on='year', how='inner')
        comparativa = comparativa[['year', 'inflacion_anual', 'acumulado_bcra']]
        
        # Mostrar comparativa
        st.dataframe(comparativa, use_container_width=True)
        
        # Gráfico comparativo
        fig3, ax3 = plt.subplots(figsize=(10, 5))
        ax3.plot(comparativa['year'], comparativa['inflacion_anual'], marker='o', label='World Bank (anual)', color='#d62728')
        ax3.plot(comparativa['year'], comparativa['acumulado_bcra'], marker='s', label='BCRA (acumulado mensual)', color='#1f77b4')
        ax3.set_xlabel("Año")
        ax3.set_ylabel("Inflación anual (%)")
        ax3.set_title("Comparación de fuentes: World Bank vs. BCRA (acumulado mensual)")
        ax3.legend()
        ax3.grid(True, linestyle='--', alpha=0.6)
        st.pyplot(fig3)
    else:
        st.info("Datos mensuales no disponibles para comparación.")

st.caption("Fuentes: Banco Mundial (inflación anual) | BCRA (inflación mensual) - Dashboard interactivo")