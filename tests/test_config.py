import pytest
import config


@pytest.fixture()
def COFNIG():
    return {}

@pytest.mark.parametrize(
    'filename',[
        'abc.json',
        '']
    )
def test_no_file(filename,COFNIG):
    # 如果文件名不存在
    config.config_file = filename
    with pytest.raises(FileNotFoundError) as e:
        config.load_config()
    assert config.CONFIG == COFNIG

# @pytest.mark.skip(reason="忽略测试")
# def test_pass():
#     assert 1 == 1