"""なろうランキング取得処理関連のテスト."""

from datetime import timedelta

import pytest

from apis.narou.type import RankType
from batch.get_ranking import process_command_args
from common.datetime_util import jst_now


# process_command_argsのテスト
def test_future_date():
    """未来日のrank_dateが指定された場合はエラー."""
    future_date = (jst_now() + timedelta(days=1)).strftime("%Y%m%d")
    args = [future_date, "d"]
    with pytest.raises(ValueError, match="rank_dateは未来日を指定できません"):
        process_command_args(args)


def test_invalid_date_format():
    """無効な日付形式が指定された場合はエラー."""
    args = ["invalid_date", "d"]
    with pytest.raises(ValueError, match="無効なrank_dateが指定されました"):
        process_command_args(args)


def test_no_argument():
    """引数が指定されていない場合は現在日時とデフォルトのrank_typeを使用."""
    args = []
    results = process_command_args(args)
    expected_date = jst_now().strftime("%Y%m%d")
    assert results[0] == expected_date
    assert results[1] == [RankType.DAILY]


def test_empty_date_argument():
    """空のrank_date引数が渡された場合は現在日とする."""
    args = ["", "d"]
    results = process_command_args(args)
    expected_date = jst_now().strftime("%Y%m%d")
    assert results[0] == expected_date
    assert results[1] == [RankType.DAILY]


def test_valid_rank_type_daily():
    """有効なrank_typeがDAILYの場合."""
    args = ["20231201", "d"]
    results = process_command_args(args)
    assert results[0] == "20231201"
    assert results[1] == [RankType.DAILY]


def test_valid_rank_type_weekly():
    """有効なrank_typeがWEEKLYの場合."""
    args = ["20231201", "w"]
    results = process_command_args(args)
    assert results[0] == "20231201"
    assert results[1] == [RankType.WEEKLY]


def test_valid_rank_type_monthly():
    """有効なrank_typeがMONTHLYの場合."""
    args = ["20231201", "m"]
    results = process_command_args(args)
    assert results[0] == "20231201"
    assert results[1] == [RankType.MONTHLY]


def test_valid_rank_type_quarterly():
    """有効なrank_typeがQUARTERLYの場合."""
    args = ["20231201", "q"]
    results = process_command_args(args)
    assert results[0] == "20231201"
    assert results[1] == [RankType.QUARTERLY]


def test_invalid_rank_type():
    """無効なrank_typeが指定された場合はエラー."""
    args = ["20231201", "invalid"]
    with pytest.raises(
        ValueError,
        match="無効なrank_typeが指定されました。許容される値: d, w, m, q",
    ):
        process_command_args(args)


def test_default_rank_type_tuesday():
    """rank_type未指定で特定の日付（2023年12月5日、火曜日）をテスト."""
    args = ["20231205"]  # 火曜日
    results = process_command_args(args)
    assert results[0] == "20231205"
    assert results[1] == [RankType.DAILY, RankType.WEEKLY]


def test_default_rank_type_first_day():
    """rank_type未指定で月初（2023年12月1日、金曜日）をテスト."""
    args = ["20231201"]  # 月初
    results = process_command_args(args)
    assert results[0] == "20231201"
    assert results[1] == [RankType.DAILY, RankType.MONTHLY, RankType.QUARTERLY]


def test_default_rank_type_normal_day():
    """rank_type未指定で火曜日でも月初でもない日（2023年12月6日、水曜日）をテスト."""
    args = ["20231206"]  # それ以外
    results = process_command_args(args)
    assert results[0] == "20231206"
    assert results[1] == [RankType.DAILY]


def test_default_rank_type_all_conditions():
    """rank_type未指定で全ての条件を満たす日（2024年10月1日、火曜日）をテスト."""
    args = ["20241001"]  # 火曜日かつ月初
    results = process_command_args(args)
    assert results[0] == "20241001"
    assert results[1] == [
        RankType.DAILY,
        RankType.WEEKLY,
        RankType.MONTHLY,
        RankType.QUARTERLY,
    ]


def test_empty_rank_type_argument_tuesday():
    """rank_typeが空文字で特定の日付（2023年12月5日、火曜日）をテスト。."""
    args = ["20231205", ""]
    results = process_command_args(args)
    assert results[0] == "20231205"
    assert results[1] == [RankType.DAILY, RankType.WEEKLY]


def test_empty_rank_type_argument_month_start():
    """rank_typeが空文字で月初（2023年12月1日、金曜日）をテスト。."""
    args = ["20231201", ""]
    results = process_command_args(args)
    assert results[0] == "20231201"
    assert results[1] == [RankType.DAILY, RankType.MONTHLY, RankType.QUARTERLY]


def test_empty_rank_type_argument_other_day():
    """rank_typeが空文字で火曜日でも月初でもない日（2023年12月6日、水曜日）をテスト。."""
    args = ["20231206", ""]
    results = process_command_args(args)
    assert results[0] == "20231206"
    assert results[1] == [RankType.DAILY]


def test_empty_rank_type_argument_all_conditions():
    """rank_typeが空文字で全ての条件を満たす日（2024年10月1日、火曜日）をテスト。."""
    args = ["20241001", ""]
    results = process_command_args(args)
    assert results[0] == "20241001"
    assert results[1] == [
        RankType.DAILY,
        RankType.WEEKLY,
        RankType.MONTHLY,
        RankType.QUARTERLY,
    ]


def test_date_before_20130501():
    """2013年5月1日以前の日付が指定された場合もエラーにはならない."""
    args = ["20130430", "d"]
    results = process_command_args(args)
    assert results[0] == "20130430"
    assert results[1] == [
        RankType.DAILY,
    ]


def test_weekly_with_invalid_day():
    """週間ランキングで火曜日以外の日付が指定された場合でもRankType.WEEKLYが含まれる."""
    args = ["20231201", "w"]  # 2023年12月1日は金曜日
    results = process_command_args(args)
    # RankType.WEEKLY が結果に含まれることを確認
    assert results[0] == "20231201"
    assert RankType.WEEKLY in results[1]


def test_monthly_with_invalid_day():
    """月間ランキングで1日以外の日付が指定された場合でもRankType.MONTHLYが含まれる."""
    args = ["20231215", "m"]  # 2023年12月15日は1日ではない
    results = process_command_args(args)
    # RankType.MONTHLY が結果に含まれることを確認
    assert results[0] == "20231215"
    assert RankType.MONTHLY in results[1]


def test_quarterly_with_invalid_day():
    """四半期ランキングで1日以外の日付が指定された場合でもRankType.QUARTERLYが含まれる."""
    args = ["20231215", "q"]  # 2023年12月15日は1日ではない
    results = process_command_args(args)
    # RankType.QUARTERLY が結果に含まれることを確認
    assert results[0] == "20231215"
    assert RankType.QUARTERLY in results[1]


def test_weekly_with_tuesday():
    """週間ランキングで火曜日が正しく処理される."""
    args = ["20231205", "w"]  # 2023年12月5日は火曜日
    results = process_command_args(args)
    assert results[0] == "20231205"
    assert results[1] == [RankType.WEEKLY]


def test_monthly_with_first_day():
    """月間ランキングで1日が正しく処理される."""
    args = ["20231201", "m"]
    results = process_command_args(args)
    assert results[0] == "20231201"
    assert results[1] == [RankType.MONTHLY]


def test_quarterly_with_first_day():
    """四半期ランキングで1日が正しく処理される."""
    args = ["20231201", "q"]
    results = process_command_args(args)
    assert results[0] == "20231201"
    assert results[1] == [RankType.QUARTERLY]
