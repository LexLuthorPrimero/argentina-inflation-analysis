import pytest
import os
import pandas as pd
from scripts.run_etl import main

def test_run_etl_genera_csv():
    # Ejecutar el ETL
    main()
    
    # Verificar que se creó el archivo CSV
    assert os.path.exists("data/raw/worldbank_inflation.csv")
    
    # Verificar que el CSV tiene datos
    df = pd.read_csv("data/raw/worldbank_inflation.csv")
    assert not df.empty
    assert 'year' in df.columns
    assert 'inflacion_anual' in df.columns