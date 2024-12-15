"""全てのランキングを投入用."""

from datetime import datetime, timedelta

from batch.get_ranking import get_ranking
from config.log import console_logger


def generate_date_strings(start_date: str):
    """20130501 ~ 現在日までの日付を yyyymmdd の形式で取得。.

    Args:
        start_date (str): 開始日 (yyyymmdd 形式)

    Returns:
        list[str]: 開始日から現在日までの日付文字列リスト。
    """
    start = datetime.strptime(start_date, "%Y%m%d")
    today = datetime.now()
    date_list = []

    while start <= today:
        date_list.append(start.strftime("%Y%m%d"))
        start += timedelta(days=1)

    return date_list


def run():
    """20130501 から現在日までの日付を生成、それぞれの日付についてランキングデータを取得.

    この関数は、`generate_date_strings` を使用して日付文字列のリストを生成し、
    各日付に対して `get_ranking` 関数を呼び出してランキングを取得します。
    """
    error_date_list = []
    for date in generate_date_strings("20130501"):
        try:
            error_date_list.append(date)
            get_ranking(date)
            error_date_list.pop()
        except Exception:
            pass
    console_logger.error(f"{error_date_list}")
