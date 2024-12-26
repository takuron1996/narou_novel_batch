"""テスト用のデータ."""

import pytest

from batch.data import NcodeMappingData


@pytest.fixture
def ncode_mapping_data_list():
    """テスト用のNcodeMappingDataのリスト."""
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
