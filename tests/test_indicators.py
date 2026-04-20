import pytest
import pandas as pd
from src.transform.calculate import calcular_variacion_anual  # necesita ajustar import

def test_calcular_variacion_anual():
    datos = pd.DataFrame({'year': [2020,2021], 'inflacion_anual': [10,20]})
    resultado = calcular_variacion_anual(datos)
    assert resultado.loc[1, 'variacion'] == 100.0