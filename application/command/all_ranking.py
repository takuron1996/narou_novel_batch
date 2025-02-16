"""全てのランキングを投入用."""

from datetime import timedelta

from batch.get_ranking import get_ranking
from common.datetime_util import jst_now, jst_strptime
from config.log import console_logger


def generate_date_strings(start_date: str):
    """20130501 ~ 現在日までの日付を yyyymmdd の形式で取得。.

    Args:
        start_date (str): 開始日 (yyyymmdd 形式)

    Returns:
        list[str]: 開始日から現在日までの日付文字列リスト。
    """
    if not start_date.isdigit() or len(start_date) != 8:
        raise ValueError("開始日は8桁の数字（YYYYMMDD）で指定してください")

    start = jst_strptime(start_date)
    today = jst_now()

    if start > today:
        raise ValueError("開始日は現在日より前の日付を指定してください")

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
            get_ranking(date)
        except Exception:
            error_date_list.append(date)
    console_logger.error(f"{error_date_list}")
