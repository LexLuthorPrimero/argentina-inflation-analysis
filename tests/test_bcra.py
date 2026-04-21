from src.extract.bcra import extract_inflation_bcra

def test_bcra_funcion_existe():
    assert callable(extract_inflation_bcra)