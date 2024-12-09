import pytest
from datetime import datetime, timedelta
from batch.daily_get_ranking import process_command_args


# process_command_argsのテスト
def test_valid_date():
    """有効なrank_dateが指定された場合"""
    args = ["script_name", "20231201"]
    result = process_command_args(args)
    assert result == "20231201"


def test_future_date():
    """未来日のrank_dateが指定された場合はエラー"""
    future_date = (datetime.now() + timedelta(days=1)).strftime("%Y%m%d")
    args = ["script_name", future_date]
    with pytest.raises(ValueError, match="rank_dateは未来日を指定できません"):
        process_command_args(args)


def test_invalid_date_format():
    """無効な日付形式が指定された場合はエラー"""
    args = ["script_name", "invalid_date"]
    with pytest.raises(ValueError, match="無効なrank_dateが指定されました"):
        process_command_args(args)


def test_no_argument():
    """引数が指定されていない場合は現在日時を使用"""
    args = ["script_name"]
    result = process_command_args(args)
    expected_date = datetime.now().strftime("%Y%m%d")
    assert result == expected_date


def test_empty_date_argument():
    """空の引数が渡された場合もエラーとする"""
    args = ["script_name", ""]
    with pytest.raises(ValueError, match="無効なrank_dateが指定されました"):
        process_command_args(args)
