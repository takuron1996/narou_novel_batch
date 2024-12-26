"""小説情報取得バッチ関連のテスト."""

from unittest.mock import Mock

import pytest

from apis.narou.narou_data import NarouData
from batch.data import NcodeMappingData
from batch.get_novel_data import fetch_novel_info, get_target_from_db


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
