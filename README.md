[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.56+-red.svg)](https://streamlit.io/)
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://argentina-inflation-analysis-gqbzvy2fjksctot5qd6vvd.streamlit.app/)
[![Coverage](https://img.shields.io/badge/coverage-91%25-brightgreen.svg)](badges/coverage.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# 📈 Análisis de inflación en Argentina

Pipeline ETL que descarga datos oficiales del BCRA (inflación mensual), los procesa y los visualiza en un dashboard interactivo con Streamlit.

## 🚀 Características

- Extracción automática desde API del BCRA (datos mensuales)
- Cálculo de inflación acumulada anual, promedios y máximos
- Dashboard con filtros por fecha, tipo de gráfico y descarga CSV
- Tests unitarios + cobertura 91%
- Integración continua (GitHub Actions)
- Contenedor Docker para fácil ejecución
- Actualización automática diaria de datos

## 🛠️ Tecnologías

- Python 3.13
- Pandas, Requests
- Streamlit
- pytest, ruff, mypy
- GitHub Actions
- Docker

## 📦 Instalación y uso

```bash
git clone https://github.com/LexLuthorPrimero/argentina-inflation-analysis.git
cd argentina-inflation-analysis
python -m venv venv
source venv/bin/activate
pip install -e .
streamlit run dashboard/app.py


🐳 Docker
docker build -t argentina-inflation .
docker run -p 8501:8501 -v $(pwd)/data:/app/data argentina-inflation


📊 Demo online

https://argentina-inflation-analysis-gqbzvy2fjksctot5qd6vvd.streamlit.app/
📄 Licencia

MIT
👤 Autor

Lucas (LexLuthorPrimero) – GitHub

