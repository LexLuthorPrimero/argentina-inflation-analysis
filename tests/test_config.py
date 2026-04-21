from src.utils import config

def test_config_vars():
    assert hasattr(config, 'DATA_RAW_PATH')
    assert hasattr(config, 'DATA_PROCESSED_PATH')
    assert hasattr(config, 'DATABASE_PATH')
    assert config.DATA_RAW_PATH == "data/raw"