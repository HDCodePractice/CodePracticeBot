import pytest
import config

@pytest.mark.parametrize(
    'filename',[
        'abc.json',
        '']
    )
def test_no_file(filename):
    # 如果文件名不存在
    config.config_file = filename
    with pytest.raises(FileNotFoundError) as e:
        config.load_config()
    assert config.CONFIG == {}

# @pytest.mark.skip(reason="忽略测试")
# def test_pass():
#     assert 1 == 1