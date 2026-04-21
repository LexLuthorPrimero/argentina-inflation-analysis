import pytest
import pandas as pd
from src.transform.calculate import calcular_variacion_anual

def test_calcular_variacion_anual():
    df = pd.DataFrame({'year': [2020,2021,2022], 'inflacion_anual': [10,20,30]})
    result = calcular_variacion_anual(df)
    assert 'variacion' in result.columns
    assert result.loc[0, 'variacion'] is None or pd.isna(result.loc[0, 'variacion'])
    assert result.loc[1, 'variacion'] == 100.0
    assert result.loc[2, 'variacion'] == 50.0