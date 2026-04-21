import requests
import pandas as pd

url = "https://api.bcra.gob.ar/estadisticas/v4.0/monetarias"
try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    if data.get("status") == 200 and "results" in data:
        results = data["results"]
        df = pd.DataFrame(results)
        # Buscamos las variables que contienen la palabra "inflación" (case-insensitive)
        inflation_vars = df[
            df["descripcion"].str.contains("inflación", case=False, na=False)
        ]
        print(inflation_vars[["idVariable", "descripcion", "periodicidad"]])
    else:
        print("Error en la respuesta de la API:", data.get("status"))
except Exception as e:
    print(f"Error al conectar con la API: {e}")
