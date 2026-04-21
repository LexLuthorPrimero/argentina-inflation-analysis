import pytest
from src.extract.worldbank import extract_inflation_worldbank


def test_extractor_devuelve_dataframe():
    df = extract_inflation_worldbank()
    assert df is not None
    assert not df.empty
    assert "year" in df.columns
    assert "inflacion_anual" in df.columns


def test_extractor_tiene_datos_argentina():
    df = extract_inflation_worldbank(country="AR", start=2020, end=2024)
    # Debería tener al menos 5 años (2020-2024)
    assert len(df) >= 5
    assert df["year"].min() >= 2020
    assert df["year"].max() <= 2024
