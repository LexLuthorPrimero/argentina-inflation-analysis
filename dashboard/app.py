import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(page_title="Inflación Argentina", layout="wide")
st.title("📊 Inflación Argentina - Dashboard Interactivo")

@st.cache_data
def load_monthly_data():
    path = Path("data/raw/bcra_inflation_monthly.csv")
    if path.exists():
        df = pd.read_csv(path)
        df['date'] = pd.to_datetime(df['date'])
        df['year'] = df['date'].dt.year
        return df
    return None

@st.cache_data
def load_annual_accumulated():
    path = Path("data/processed/inflacion_mensual_acumulada.csv")
    if path.exists():
        df = pd.read_csv(path)
        df.rename(columns={'year': 'year', 'inflacion_mensual': 'inflacion_anual'}, inplace=True)
        return df
    return None

df_mensual = load_monthly_data()
df_anual = load_annual_accumulated()

if df_anual is None:
    st.error("No se encontraron datos acumulados anuales. Ejecuta 'python scripts/run_analysis_monthly.py'")
    st.stop()

st.sidebar.header("⚙️ Configuración")

tab1, tab2, tab3 = st.tabs(["📈 Inflación Anual (BCRA acumulado)", "📉 Inflación Mensual (BCRA)", "📊 Comparación"])

# Tab 1: Anual (acumulado BCRA)
with tab1:
    st.subheader("Inflación anual acumulada (datos mensuales BCRA)")
    min_year = int(df_anual['year'].min())
    max_year = int(df_anual['year'].max())
    year_range = st.slider("Seleccionar rango de años", min_year, max_year, (min_year, max_year), key="anual_range")
    df_filtrado = df_anual[(df_anual['year'] >= year_range[0]) & (df_anual['year'] <= year_range[1])]
    chart_type = st.radio("Tipo de gráfico", ["Línea", "Barras", "Ambos"], horizontal=True, key="anual_chart")
    fig, ax = plt.subplots(figsize=(10,5))
    if chart_type in ["Línea", "Ambos"]:
        ax.plot(df_filtrado['year'], df_filtrado['inflacion_anual'], marker='o', color='#d62728', label='Inflación anual')
    if chart_type in ["Barras", "Ambos"]:
        ax.bar(df_filtrado['year'], df_filtrado['inflacion_anual'], alpha=0.5, color='#ff7f0e', label='Inflación anual')
    ax.set_xlabel("Año")
    ax.set_ylabel("Inflación anual acumulada (%)")
    ax.set_title(f"Evolución de la inflación anual acumulada ({year_range[0]}-{year_range[1]})")
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend()
    st.pyplot(fig)
    if st.checkbox("Mostrar tabla", value=True, key="anual_table"):
        st.dataframe(df_filtrado, use_container_width=True)
    csv = df_filtrado.to_csv(index=False)
    st.download_button("📥 Descargar datos anuales (CSV)", csv, "inflacion_anual_acumulada.csv", "text/csv")

# Tab 2: Mensual (igual que antes, pero usando df_mensual)
with tab2:
    if df_mensual is None:
        st.warning("Datos mensuales no disponibles.")
    else:
        st.subheader("Inflación mensual (BCRA)")
        min_date = df_mensual['date'].min().date()
        max_date = df_mensual['date'].max().date()
        date_range = st.slider("Seleccionar rango de fechas", min_date, max_date, (min_date, max_date), format="YYYY-MM", key="mensual_range")
        df_filtrado_m = df_mensual[(df_mensual['date'].dt.date >= date_range[0]) & (df_mensual['date'].dt.date <= date_range[1])]
        chart_type_m = st.radio("Tipo de gráfico", ["Línea", "Barras", "Ambos"], horizontal=True, key="mensual_chart")
        fig2, ax2 = plt.subplots(figsize=(12,5))
        if chart_type_m in ["Línea", "Ambos"]:
            ax2.plot(df_filtrado_m['date'], df_filtrado_m['inflacion_mensual'], marker='.', color='#1f77b4', label='Inflación mensual')
        if chart_type_m in ["Barras", "Ambos"]:
            ax2.bar(df_filtrado_m['date'], df_filtrado_m['inflacion_mensual'], width=20, alpha=0.5, color='#2ca02c', label='Inflación mensual')
        ax2.set_xlabel("Fecha")
        ax2.set_ylabel("Variación mensual (%)")
        ax2.set_title("Inflación mensual Argentina")
        ax2.grid(True, linestyle='--', alpha=0.6)
        ax2.legend()
        st.pyplot(fig2)
        col1, col2, col3 = st.columns(3)
        ultimo_mes = df_filtrado_m.iloc[-1]
        col1.metric("Último mes", ultimo_mes['date'].strftime('%Y-%m'), f"{ultimo_mes['inflacion_mensual']:.2f}%")
        max_mensual = df_filtrado_m['inflacion_mensual'].max()
        col2.metric("Máximo mensual", f"{max_mensual:.2f}%", delta=None)
        promedio_mensual = df_filtrado_m['inflacion_mensual'].mean()
        col3.metric("Promedio mensual", f"{promedio_mensual:.2f}%", delta=None)
        if st.checkbox("Mostrar tabla mensual", value=True, key="mensual_table"):
            st.dataframe(df_filtrado_m, use_container_width=True)
        csv_m = df_filtrado_m.to_csv(index=False)
        st.download_button("📥 Descargar datos mensuales (CSV)", csv_m, "inflacion_mensual.csv", "text/csv")

# Tab 3: Comparación (puedes dejarla igual o simplificarla)
with tab3:
    st.subheader("Comparación: Inflación anual acumulada vs. mensual")
    st.info("La inflación anual acumulada se calcula a partir de los datos mensuales del BCRA.")
    if df_anual is not None:
        st.dataframe(df_anual, use_container_width=True)

st.caption("Fuente: BCRA a través de estadisticasbcra.com | Dashboard interactivo")