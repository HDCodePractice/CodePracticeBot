import config

def test_load_config():
    config.config_file = "config.json"
    config.load_config()
    assert config.CONFIG == {}