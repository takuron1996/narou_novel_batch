import pytest
from unittest.mock import Mock
from apis.narou.narou_data import NarouRankData, NarouRankDataMapper


@pytest.fixture
def valid_response_mock():
    """正常なレスポンスデータをモックする"""
    response_mock = Mock()
    response_mock.json.return_value = [
        {"ncode": "N6682GF", "pt": 144, "rank": 300},
        {"ncode": "N1234AB", "pt": 200, "rank": 150},
    ]
    return response_mock


@pytest.fixture
def invalid_response_mock():
    """無効なレスポンスデータをモックする"""
    response_mock = Mock()
    response_mock.json.return_value = [{"ncode": "N6682GF"}]
    return response_mock


@pytest.fixture
def empty_response_mock():
    """空のレスポンスデータをモックする"""
    response_mock = Mock()
    response_mock.json.return_value = []
    return response_mock


@pytest.fixture
def invalid_json_mock():
    """JSON解析が失敗するレスポンスをモックする"""
    response_mock = Mock()
    response_mock.json.side_effect = ValueError("Invalid JSON")
    return response_mock


def test_map_response_to_data_with_valid_response(valid_response_mock):
    """正常なレスポンスデータをマッピングするテスト"""
    result = NarouRankDataMapper.map_response_to_data(valid_response_mock)
    assert len(result) == 2
    assert isinstance(result[0], NarouRankData)
    assert result[0].ncode == "N6682GF"
    assert result[0].pt == 144
    assert result[0].rank == 300


def test_map_response_to_data_with_invalid_response(invalid_response_mock):
    """無効なレスポンスデータで例外が発生することを確認するテスト"""
    with pytest.raises(ValueError) as excinfo:
        NarouRankDataMapper.map_response_to_data(invalid_response_mock)
    assert (
        "NarouRankData.__init__() missing 2 required positional arguments: 'pt' and 'rank'"
        in str(excinfo.value)
    )
