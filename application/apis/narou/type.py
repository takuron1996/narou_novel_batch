"""なろうランキングのEnum関連."""

from datetime import datetime
from enum import Enum

from config.log import console_logger


class RankType(Enum):
    """なろうランキングのrtype."""

    DAILY = "d"
    WEEKLY = "w"
    MONTHLY = "m"
    QUARTERLY = "q"

    @staticmethod
    def is_valid_date_for_rank_type(rank_type, date):
        """指定されたランキング種別に対して、日付が有効かどうかを検証します。.

        引数:
            rank_type (RankType): 検証するランキング種別。
                `RankType` のいずれかの値でなければなりません。
            date (str): 検証する日付（フォーマット: "YYYYMMDD"）。

        戻り値:
            bool: 日付が指定されたランキング種別に適合する場合はTrue、それ以外はFalse。

        検証ルール:
            - `RankType.WEEKLY` の場合: 日付が火曜日でなければなりません。
            - `RankType.MONTHLY` または `RankType.QUARTERLY` の場合:
                 日付が月の1日でなければなりません。
            - 日付が2013年5月1日以降でなければなりません。
            - 無効な形式の日付が指定された場合やルールに違反した場合、
                エラーメッセージがログに記録されます。

        例外:
            - `ValueError`: 引数 `date` が無効な形式の場合に発生します。

        使用例:
            ```python
            valid = RankType.is_valid_date_for_rank_type(RankType.WEEKLY, "20231205")
            print(valid)  # True（火曜日の日付であれば有効）
            ```
        """
        try:
            parsed_date = datetime.strptime(date, "%Y%m%d")
            if rank_type == RankType.WEEKLY and parsed_date.weekday() != 1:
                console_logger.error(
                    "週間を指定する場合の日付は火曜日の日付を指定"
                )
                return False
            elif (
                rank_type in (RankType.MONTHLY, RankType.QUARTERLY)
                and parsed_date.day != 1
            ):
                console_logger.error(
                    "月間、四半期を取得する場合、日付は1日を指定"
                )
                return False
            elif parsed_date < datetime(2013, 5, 1):
                console_logger.error("2013年5月1日以降の日付を指定")
                return False
            return True
        except ValueError:
            console_logger.error(f"日付 {date} は無効な形式です。")
            return False


class OutType(Enum):
    """なろうランキングout."""

    YAML = "yaml"
    JSON = "json"
    PHP = "php"
