import pytest
from datetime import datetime, timedelta
from batch.daily_get_ranking import process_command_args
from apis.narou.type import RankType

# process_command_argsのテスト
def test_future_date():
    """未来日のrank_dateが指定された場合はエラー"""
    future_date = (datetime.now() + timedelta(days=1)).strftime("%Y%m%d")
    args = [future_date, "d"]
    with pytest.raises(ValueError, match="rank_dateは未来日を指定できません"):
        process_command_args(args)


def test_invalid_date_format():
    """無効な日付形式が指定された場合はエラー"""
    args = ["invalid_date", "d"]
    with pytest.raises(ValueError, match="無効なrank_dateが指定されました"):
        process_command_args(args)


def test_no_argument():
    """引数が指定されていない場合は現在日時とデフォルトのrank_typeを使用"""
    args = []
    results = process_command_args(args)
    expected_date = datetime.now().strftime("%Y%m%d")
    assert results[0] == expected_date
    assert results[1] == RankType.DAILY


def test_empty_date_argument():
    """空のrank_date引数が渡された場合はエラーとする"""
    args = ["", "d"]
    with pytest.raises(ValueError, match="無効なrank_dateが指定されました"):
        process_command_args(args)

def test_valid_rank_type_daily():
    """有効なrank_typeがDAILYの場合"""
    args = ["20231201", "d"]
    results = process_command_args(args)
    assert results[0] == "20231201"
    assert results[1] == RankType.DAILY


def test_valid_rank_type_weekly():
    """有効なrank_typeがWEEKLYの場合"""
    args = ["20231201", "w"]
    results = process_command_args(args)
    assert results[0] == "20231201"
    assert results[1] == RankType.WEEKLY


def test_valid_rank_type_monthly():
    """有効なrank_typeがMONTHLYの場合"""
    args = ["20231201", "m"]
    results = process_command_args(args)
    assert results[0] == "20231201"
    assert results[1] == RankType.MONTHLY


def test_valid_rank_type_quarterly():
    """有効なrank_typeがQUARTERLYの場合"""
    args = ["20231201", "q"]
    results = process_command_args(args)
    assert results[0] == "20231201"
    assert results[1] == RankType.QUARTERLY

def test_invalid_rank_type():
    """無効なrank_typeが指定された場合はエラー"""
    args = ["20231201", "invalid"]
    with pytest.raises(ValueError, match="無効なrank_typeが指定されました。許容される値: d, w, m, q"):
        process_command_args(args)


def test_default_rank_type():
    """rank_typeが指定されていない場合はデフォルト値を使用"""
    args = ["20231201"]
    results = process_command_args(args)
    assert results[0] == "20231201"
    assert results[1] == RankType.DAILY

def test_empty_rank_type_argument():
    """rank_typeが空文字の場合はエラーとする"""
    args = ["20231201", ""]
    with pytest.raises(ValueError, match="無効なrank_typeが指定されました。許容される値: d, w, m, q"):
        process_command_args(args)