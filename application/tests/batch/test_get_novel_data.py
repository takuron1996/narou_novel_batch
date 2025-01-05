"""小説情報取得バッチ関連のテスト."""

from unittest.mock import Mock

import pytest

from apis.narou.narou_data import NarouData
from batch.data import NcodeMappingData
from batch.get_novel_data import (
    fetch_novel_info,
    get_chunk_list,
    get_insert_author_novel_list,
    get_insert_keyword_list,
    get_insert_novel_keyword_list,
    get_target_from_db,
)


@pytest.fixture
def insert_data_list():
    """登録したい小説情報."""
    return [
        NarouData(
            id="d661e054-e78e-4bdc-8e0f-22c046063f5c",
            title="前世は魔女でした！",
            userid=1111111,
            ncode="N1121JW",
            writer="カレヤタミエ",
            biggenre=2,
            genre=201,
            keyword="A1 A2 A3   A4",
            noveltype=1,
            isr15=0,
            isbl=0,
            isgl=0,
            iszankoku=0,
            istensei=0,
            istenni=0,
        ),
        NarouData(
            id="8e938824-9797-4e2c-bdbd-3e88e7df5b96",
            title="次の婚約者は人の気持ちのわからないサイコパスです",
            userid=2222222,
            ncode="N0563JW",
            writer="紺青",
            biggenre=1,
            genre=101,
            keyword="A4 A5",
            noveltype=2,
            isr15=1,
            isbl=1,
            isgl=1,
            iszankoku=1,
            istensei=1,
            istenni=1,
        ),
    ]


# get_target_from_db
def test_get_target_from_db(mocker):
    """正常系のケース."""
    mock_value = [
        {"id": "d661e054-e78e-4bdc-8e0f-22c046063f5c", "ncode": "N1121JW"},
        {"id": "8e938824-9797-4e2c-bdbd-3e88e7df5b96", "ncode": "N0563JW"},
    ]
    mocker.patch(
        "batch.get_novel_data.get_target_novel_data", return_value=mock_value
    )
    data_list = get_target_from_db.fn()
    assert len(data_list) == 2
    assert data_list == [
        NcodeMappingData(
            id="d661e054-e78e-4bdc-8e0f-22c046063f5c", ncode="N1121JW"
        ),
        NcodeMappingData(
            id="8e938824-9797-4e2c-bdbd-3e88e7df5b96", ncode="N0563JW"
        ),
    ]


def test_get_target_from_db_empty(mocker):
    """DBから取得したデータが空のケース."""
    mocker.patch("batch.get_novel_data.get_target_novel_data", return_value=[])
    data_list = get_target_from_db.fn()
    assert data_list == []


# fetch_novel_info
def test_fetch_novel_info(
    mocker, narou_response_value, ncode_mapping_data_list
):
    """正常系のケース."""
    response_mock = Mock()
    response_mock.json.return_value = narou_response_value
    mocker.patch("batch.get_novel_data.request_get", return_value=response_mock)
    insert_data_list = fetch_novel_info.fn(ncode_mapping_data_list)
    assert len(insert_data_list) == 2
    assert isinstance(insert_data_list[0], NarouData)

    # 1番目のデータ
    assert insert_data_list[0].id == ncode_mapping_data_list[0].id
    assert insert_data_list[0].title == narou_response_value[1].get("title")
    assert insert_data_list[0].userid == narou_response_value[1].get("userid")
    assert insert_data_list[0].ncode == ncode_mapping_data_list[0].ncode
    assert insert_data_list[0].writer == narou_response_value[1].get("writer")
    assert insert_data_list[0].biggenre == narou_response_value[1].get(
        "biggenre"
    )
    assert insert_data_list[0].genre == narou_response_value[1].get("genre")
    assert insert_data_list[0].keyword == narou_response_value[1].get("keyword")
    assert insert_data_list[0].noveltype == narou_response_value[1].get(
        "noveltype"
    )
    assert insert_data_list[0].isr15 == narou_response_value[1].get("isr15")
    assert insert_data_list[0].isbl == narou_response_value[1].get("isbl")
    assert insert_data_list[0].isgl == narou_response_value[1].get("isgl")
    assert insert_data_list[0].iszankoku == narou_response_value[1].get(
        "iszankoku"
    )
    assert insert_data_list[0].istensei == narou_response_value[1].get(
        "istensei"
    )
    assert insert_data_list[0].istenni == narou_response_value[1].get("istenni")

    # 2番目のデータ
    assert insert_data_list[1].id == ncode_mapping_data_list[1].id
    assert insert_data_list[1].title == narou_response_value[2].get("title")
    assert insert_data_list[1].userid == narou_response_value[2].get("userid")
    assert insert_data_list[1].ncode == ncode_mapping_data_list[1].ncode
    assert insert_data_list[1].writer == narou_response_value[2].get("writer")
    assert insert_data_list[1].biggenre == narou_response_value[2].get(
        "biggenre"
    )
    assert insert_data_list[1].genre == narou_response_value[2].get("genre")
    assert insert_data_list[1].keyword == narou_response_value[2].get("keyword")
    assert insert_data_list[1].noveltype == narou_response_value[2].get(
        "noveltype"
    )
    assert insert_data_list[1].isr15 == narou_response_value[2].get("isr15")
    assert insert_data_list[1].isbl == narou_response_value[2].get("isbl")
    assert insert_data_list[1].isgl == narou_response_value[2].get("isgl")
    assert insert_data_list[1].iszankoku == narou_response_value[2].get(
        "iszankoku"
    )
    assert insert_data_list[1].istensei == narou_response_value[2].get(
        "istensei"
    )
    assert insert_data_list[1].istenni == narou_response_value[2].get("istenni")


def test_invalid_fetch_novel_info(mocker, ncode_mapping_data_list):
    """responseが200以外の場合のケース."""
    mocker.patch("batch.get_novel_data.request_get", return_value=None)
    with pytest.raises(Exception) as excinfo:
        fetch_novel_info.fn(ncode_mapping_data_list)
    assert ("レスポンスが200以外のため終了") in str(excinfo.value)


def test_fetch_novel_info_empty_list_arg():
    """引数が空リストの場合の処理."""
    results = fetch_novel_info.fn([])
    assert results == []


# insert_novel_into_db関連
def test_get_insert_keyword_list(insert_data_list):
    """正常系のテスト."""
    results = get_insert_keyword_list(insert_data_list)
    results.sort(key=lambda x: x.get("name"))
    assert len(results) == 5
    assert results[0].get("keyword_id")[:7] == "KEYWORD"
    assert len(results[0].get("keyword_id")) == 43
    assert results[0].get("name") == "A1"
    assert len(results[1].get("keyword_id")) == 43
    assert results[1].get("name") == "A2"
    assert len(results[2].get("keyword_id")) == 43
    assert results[2].get("name") == "A3"
    assert len(results[3].get("keyword_id")) == 43
    assert results[3].get("name") == "A4"
    assert len(results[4].get("keyword_id")) == 43
    assert results[4].get("name") == "A5"


def test_get_insert_author_novel_list(insert_data_list):
    """正常系のテスト."""
    results = get_insert_author_novel_list(insert_data_list)
    results.sort(key=lambda x: x.get("userid"))
    assert len(results) == 2
    assert results[0].get("userid") == insert_data_list[0].userid
    assert results[0].get("writer") == insert_data_list[0].writer
    assert results[0].get("author_id")[:6] == "AUTHOR"
    assert len(results[0].get("author_id")) == 42
    assert results[0].get("id") == insert_data_list[0].id
    assert results[0].get("title") == insert_data_list[0].title
    assert results[0].get("biggenre_code") == insert_data_list[0].biggenre
    assert results[0].get("genre_code") == insert_data_list[0].genre
    assert results[0].get("novel_type_id") == insert_data_list[0].noveltype
    assert not results[0].get("isr15")
    assert not results[0].get("isbl")
    assert not results[0].get("isgl")
    assert not results[0].get("iszankoku")
    assert not results[0].get("istensei")
    assert not results[0].get("istenni")

    assert results[1].get("userid") == insert_data_list[1].userid
    assert results[1].get("writer") == insert_data_list[1].writer
    assert len(results[1].get("author_id")) == 42
    assert results[1].get("id") == insert_data_list[1].id
    assert results[1].get("title") == insert_data_list[1].title
    assert results[1].get("biggenre_code") == insert_data_list[1].biggenre
    assert results[1].get("genre_code") == insert_data_list[1].genre
    assert results[1].get("novel_type_id") == insert_data_list[1].noveltype
    assert results[1].get("isr15")
    assert results[1].get("isbl")
    assert results[1].get("isgl")
    assert results[1].get("iszankoku")
    assert results[1].get("istensei")
    assert results[1].get("istenni")


def test_get_insert_novel_keyword_list(insert_data_list):
    """正常系のテスト."""
    results = get_insert_novel_keyword_list(insert_data_list)
    results.sort(key=lambda x: x.get("keyword"))
    assert len(results) == 6
    assert results[0].get("id") == insert_data_list[0].id
    assert results[0].get("keyword") == "A1"
    assert results[1].get("id") == insert_data_list[0].id
    assert results[1].get("keyword") == "A2"
    assert results[2].get("id") == insert_data_list[0].id
    assert results[2].get("keyword") == "A3"
    assert results[3].get("id") == insert_data_list[0].id
    assert results[3].get("keyword") == "A4"
    assert results[4].get("id") == insert_data_list[1].id
    assert results[4].get("keyword") == "A4"
    assert results[5].get("id") == insert_data_list[1].id
    assert results[5].get("keyword") == "A5"


# get_chunk_list関連


def test_get_chunk_list():
    """正常系のテスト."""
    # 1から1999までのリスト
    large_list = list(range(1, 2000))

    chunk_data_list = get_chunk_list(large_list, 500)

    assert len(chunk_data_list) == 4
    assert len(chunk_data_list[0]) == 500
    assert len(chunk_data_list[1]) == 500
    assert len(chunk_data_list[2]) == 500
    assert len(chunk_data_list[3]) == 499


def test_below_500_get_chunk_list():
    """500未満の場合のテスト."""
    # 1から499までのリスト
    large_list = list(range(1, 500))

    chunk_data_list = get_chunk_list(large_list, 500)

    assert len(chunk_data_list) == 1
    assert len(chunk_data_list[0]) == 499
