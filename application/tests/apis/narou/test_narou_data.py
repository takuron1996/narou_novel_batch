import pytest
from unittest.mock import Mock
from apis.narou.narou_data import NarouRankData, NarouRankDataMapper
import datetime
from apis.narou.type import RankType


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


def test_map_response_to_data_with_valid_response(valid_response_mock):
    """正常なレスポンスデータをマッピングするテスト"""
    result = NarouRankDataMapper.map_response_to_data(
        valid_response_mock, "20230501", RankType.DAILY
    )
    assert len(result) == 2
    assert isinstance(result[0], NarouRankData)
    assert result[0].ncode == "N6682GF"
    assert result[0].pt == 144
    assert result[0].rank == 300
    assert result[0].rank_date == datetime.date(2023, 5, 1)
    assert len(result[0].id) == 36
    assert result[0].rank_type == "d"


def test_map_response_to_data_with_invalid_response(invalid_response_mock):
    """無効なレスポンスデータで例外が発生することを確認するテスト"""
    with pytest.raises(ValueError) as excinfo:
        NarouRankDataMapper.map_response_to_data(
            invalid_response_mock, "20230501", RankType.DAILY
        )
    assert (
        "NarouRankData.__init__() missing 2 required positional arguments: 'pt' and 'rank'"
        in str(excinfo.value)
    )
