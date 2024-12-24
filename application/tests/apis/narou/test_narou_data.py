"""narou_data.py関連のテスト."""

import datetime
from unittest.mock import Mock

import pytest

from apis.narou.narou_data import (
    NarouData,
    NarouDataMapper,
    NarouRankData,
    NarouRankDataMapper,
)
from apis.narou.type import RankType
from batch.data import NcodeMappingData


# NarouDataMapper
@pytest.fixture
def data_list():
    """テスト用のデータ."""
    return [
        NcodeMappingData(
            id="d661e054-e78e-4bdc-8e0f-22c046063f5c", ncode="N1121JW"
        ),
        NcodeMappingData(
            id="8e938824-9797-4e2c-bdbd-3e88e7df5b96", ncode="N0563JW"
        ),
    ]


@pytest.fixture
def narou_response_value():
    """なろうAPIのレスポンスの値."""
    return [
        {"allcount": 2},
        {
            "title": "前世は魔女でした！",
            "userid": 2055121,
            "ncode": "N1121JW",
            "writer": "カレヤタミエ",
            "biggenre": 2,
            "genre": 201,
            "keyword": "女主人公 魔女 R15 異世界転生",
            "noveltype": 1,
            "isr15": 1,
            "isbl": 0,
            "isgl": 0,
            "iszankoku": 0,
            "istensei": 1,
            "istenni": 0,
        },
        {
            "title": "次の婚約者は人の気持ちのわからないサイコパスです",
            "userid": 1877427,
            "writer": "紺青",
            "ncode": "N0563JW",
            "biggenre": 1,
            "genre": 101,
            "keyword": "ほのぼの ハッピーエンド 婚約破棄 人形令嬢 サイコパス令息？ R15",
            "noveltype": 2,
            "isr15": 1,
            "isbl": 0,
            "isgl": 0,
            "iszankoku": 0,
            "istensei": 0,
            "istenni": 0,
        },
    ]


@pytest.fixture
def valid_narou_response_mock(narou_response_value):
    """なろうAPIの正常なレスポンスデータをモックする."""
    response_mock = Mock()
    response_mock.json.return_value = narou_response_value
    return response_mock


@pytest.fixture
def invalid_not_ncode_narou_response_mock():
    """なろうAPIで指定したncodeがなかった場合のレスポンスデータをモックする."""
    response_mock = Mock()
    response_mock.json.return_value = [{"allcount": 0}]
    return response_mock


@pytest.fixture
def invalid_narou_response_mock():
    """なろうAPIの無効なレスポンスデータをモックする."""
    response_mock = Mock()
    response_mock.json.return_value = [{"allcount": 0}, {"ncode": "N1121JW"}]
    return response_mock


def test_narou_data_mapper_map_response_to_data_with_valid_response(
    valid_narou_response_mock, data_list, narou_response_value
):
    """正常なレスポンスデータをマッピングするテスト."""
    result = NarouDataMapper.map_response_to_data(
        valid_narou_response_mock, data_list
    )
    assert len(result) == 2
    assert isinstance(result[0], NarouData)

    # 1番目のデータ
    assert result[0].id == data_list[0].id
    assert result[0].title == narou_response_value[1].get("title")
    assert result[0].userid == narou_response_value[1].get("userid")
    assert result[0].ncode == data_list[0].ncode
    assert result[0].writer == narou_response_value[1].get("writer")
    assert result[0].biggenre == narou_response_value[1].get("biggenre")
    assert result[0].genre == narou_response_value[1].get("genre")
    assert result[0].keyword == narou_response_value[1].get("keyword")
    assert result[0].noveltype == narou_response_value[1].get("noveltype")
    assert result[0].isr15 == narou_response_value[1].get("isr15")
    assert result[0].isbl == narou_response_value[1].get("isbl")
    assert result[0].isgl == narou_response_value[1].get("isgl")
    assert result[0].iszankoku == narou_response_value[1].get("iszankoku")
    assert result[0].istensei == narou_response_value[1].get("istensei")
    assert result[0].istenni == narou_response_value[1].get("istenni")

    # 2番目のデータ
    assert result[1].id == data_list[1].id
    assert result[1].title == narou_response_value[2].get("title")
    assert result[1].userid == narou_response_value[2].get("userid")
    assert result[1].ncode == data_list[1].ncode
    assert result[1].writer == narou_response_value[2].get("writer")
    assert result[1].biggenre == narou_response_value[2].get("biggenre")
    assert result[1].genre == narou_response_value[2].get("genre")
    assert result[1].keyword == narou_response_value[2].get("keyword")
    assert result[1].noveltype == narou_response_value[2].get("noveltype")
    assert result[1].isr15 == narou_response_value[2].get("isr15")
    assert result[1].isbl == narou_response_value[2].get("isbl")
    assert result[1].isgl == narou_response_value[2].get("isgl")
    assert result[1].iszankoku == narou_response_value[2].get("iszankoku")
    assert result[1].istensei == narou_response_value[2].get("istensei")
    assert result[1].istenni == narou_response_value[2].get("istenni")


def test_narou_data_mapper_map_response_to_data_without_ncode(
    valid_narou_response_mock, narou_response_value, data_list
):
    """対応するncodeがない場合のテスト."""
    data_list = data_list[1:]
    result = NarouDataMapper.map_response_to_data(
        valid_narou_response_mock, data_list
    )

    assert result[0].id == data_list[0].id
    assert result[0].title == narou_response_value[2].get("title")
    assert result[0].userid == narou_response_value[2].get("userid")
    assert result[0].ncode == data_list[0].ncode
    assert result[0].writer == narou_response_value[2].get("writer")
    assert result[0].biggenre == narou_response_value[2].get("biggenre")
    assert result[0].genre == narou_response_value[2].get("genre")
    assert result[0].keyword == narou_response_value[2].get("keyword")
    assert result[0].noveltype == narou_response_value[2].get("noveltype")
    assert result[0].isr15 == narou_response_value[2].get("isr15")
    assert result[0].isbl == narou_response_value[2].get("isbl")
    assert result[0].isgl == narou_response_value[2].get("isgl")
    assert result[0].iszankoku == narou_response_value[2].get("iszankoku")
    assert result[0].istensei == narou_response_value[2].get("istensei")
    assert result[0].istenni == narou_response_value[2].get("istenni")


def test_narou_data_mapper_map_response_to_data_without_ncode_response(
    invalid_not_ncode_narou_response_mock, data_list
):
    """対応するnocdeがない場合のレスポンスデータで例外が発生することを確認するテスト."""
    result = NarouDataMapper.map_response_to_data(
        invalid_not_ncode_narou_response_mock, data_list
    )
    assert not result


def test_narou_data_mapper_map_response_to_data_with_invalid_response(
    invalid_narou_response_mock, data_list
):
    """無効なレスポンスデータで例外が発生することを確認するテスト."""
    with pytest.raises(ValueError) as excinfo:
        NarouDataMapper.map_response_to_data(
            invalid_narou_response_mock, data_list
        )
    assert (
        "NarouData.__init__() missing 13 required positional arguments: "
        "'title', 'userid', 'writer', 'biggenre', 'genre', 'keyword', "
        "'noveltype', 'isr15', 'isbl', 'isgl', 'iszankoku', 'istensei', and 'istenni'"
    ) in str(excinfo.value)


# NarouRankDataMapper


@pytest.fixture
def valid_response_mock():
    """正常なレスポンスデータをモックする."""
    response_mock = Mock()
    response_mock.json.return_value = [
        {"ncode": "N6682GF", "pt": 144, "rank": 300},
        {"ncode": "N1234AB", "pt": 200, "rank": 150},
    ]
    return response_mock


@pytest.fixture
def invalid_response_mock():
    """無効なレスポンスデータをモックする."""
    response_mock = Mock()
    response_mock.json.return_value = [{"ncode": "N6682GF"}]
    return response_mock


def test_map_response_to_data_with_valid_response(valid_response_mock):
    """正常なレスポンスデータをマッピングするテスト."""
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
    """無効なレスポンスデータで例外が発生することを確認するテスト."""
    with pytest.raises(ValueError) as excinfo:
        NarouRankDataMapper.map_response_to_data(
            invalid_response_mock, "20230501", RankType.DAILY
        )
    assert (
        "NarouRankData.__init__() "
        "missing 2 required positional arguments: 'pt' and 'rank'"
    ) in str(excinfo.value)
