"""datetime関連."""

from datetime import datetime
from zoneinfo import ZoneInfo


def jst_strptime(date_string, format="%Y%m%d"):
    """文字列をJST (日本標準時) タイムゾーン付きのdatetimeオブジェクトに変換."""
    return datetime.strptime(date_string, format).replace(
        tzinfo=ZoneInfo("Asia/Tokyo")
    )


def jst_now():
    """現在の時刻をJST (日本標準時) タイムゾーン付きの datetime オブジェクトとして返す."""
    return datetime.now(ZoneInfo("Asia/Tokyo"))
