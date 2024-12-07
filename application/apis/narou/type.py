from enum import Enum
from datetime import datetime
from config.log import console_logger


class RankType(Enum):
    """なろうランキングのrtype"""

    DAILY = "d"
    WEEKLY = "w"
    MONTHLY = "m"
    QUARTERLY = "q"

    @staticmethod
    def is_valid_date_for_rank_type(rank_type, date):
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
    """なろうランキングout"""

    YAML = "yaml"
    JSON = "json"
    PHP = "php"
