import pytest
import config

def test_no_file():
    # 如果文件名不存在
    config.config_file = "abc.json"
    with pytest.raises(FileNotFoundError) as e:
        config.load_config()
    assert config.CONFIG == {}