import pytest
from apis.narou.type import RankType, OutType


@pytest.mark.parametrize(
    "rank_type, date, expected_result",
    [
        (RankType.DAILY, "20130501", True),  # 正常な日付（日間：2013年5月1日）
        (RankType.WEEKLY, "20231205", True),  # 正常な日付（週間: 火曜日）
        (RankType.WEEKLY, "20231204", False),  # 無効な日付（週間: 月曜日）
        (RankType.MONTHLY, "20231201", True),  # 正常な日付（月間: 1日）
        (RankType.MONTHLY, "20231202", False),  # 無効な日付（月間: 2日）
        (RankType.QUARTERLY, "20231001", True),  # 正常な日付（四半期: 1日）
        (RankType.QUARTERLY, "20231002", False),  # 無効な日付（四半期: 2日）
        (RankType.DAILY, "20130430", False),  # 無効な日付（2013年5月1日より前）
        (RankType.DAILY, "invalid_date", False),  # 無効な日付形式
    ],
)
def test_rank_type_is_valid_date(rank_type, date, expected_result):
    """RankTypeのis_valid_date_for_rank_typeメソッドのテスト"""
    assert (
        RankType.is_valid_date_for_rank_type(rank_type, date) == expected_result
    )


def test_out_type():
    """OutTypeの基本動作をテスト"""
    assert OutType.JSON.value == "json"
    assert OutType.YAML.value == "yaml"
    assert OutType.PHP.value == "php"
    assert list(OutType) == [OutType.YAML, OutType.JSON, OutType.PHP]


def test_rank_type_members():
    """RankTypeのメンバーが正しいかをテスト"""
    assert RankType.DAILY.value == "d"
    assert RankType.WEEKLY.value == "w"
    assert RankType.MONTHLY.value == "m"
    assert RankType.QUARTERLY.value == "q"
    assert list(RankType) == [
        RankType.DAILY,
        RankType.WEEKLY,
        RankType.MONTHLY,
        RankType.QUARTERLY,
    ]
