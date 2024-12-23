"""なろうランキングのEnum関連."""

from enum import Enum

from common.datetime_util import jst_strptime
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
            parsed_date = jst_strptime(date)
            if rank_type == RankType.WEEKLY and parsed_date.weekday() != 1:
                console_logger.warning(
                    "週間を指定する場合の日付は火曜日の日付を指定"
                )
                return False
            elif (
                rank_type in (RankType.MONTHLY, RankType.QUARTERLY)
                and parsed_date.day != 1
            ):
                console_logger.warning(
                    "月間、四半期を取得する場合、日付は1日を指定"
                )
                return False
            elif parsed_date < jst_strptime("20130501"):
                console_logger.warning("2013年5月1日以降の日付を指定")
                return False
            return True
        except ValueError:
            console_logger.warning(f"日付 {date} は無効な形式です。")
            return False


class OutType(Enum):
    """なろうAPI関連のout."""

    YAML = "yaml"
    JSON = "json"
    PHP = "php"


class NarouOrderType(Enum):
    """なろうAPIの出力順序."""

    NEW = "new"
    FAVNOVELCNT = "favnovelcnt"
    REVIEWCNT = "reviewcnt"
    HYOKA = "hyoka"
    HYOKAASC = "hyokaasc"
    DAILYPOINT = "dailypoint"
    WEEKLYPOINT = "weeklypoint"
    MONTHLYPOINT = "monthlypoint"
    QUARTERPOINT = "quarterpoint"
    YEARLYPOINT = "yearlypoint"
    IMPRESSIONCNT = "impressioncnt"
    HYOKACNT = "hyokacnt"
    HYOKACNTASC = "hyokacntasc"
    WEEKLY = "weekly"
    LENGTHDESC = "lengthdesc"
    LENGTHASC = "lengthasc"
    GENERALFIRSTUP = "generalfirstup"
    NCODEDESC = "ncodedesc"
    OLD = "old"


class NarouOfType(Enum):
    """なろうAPIで出力する項目."""

    TITLE = "t"
    NCODE = "n"
    USERID = "u"
    WRITER = "w"
    STORY = "s"
    BIGGENRE = "bg"
    GENRE = "g"
    KEYWORD = "k"
    GENERAL_FIRSTUP = "gf"
    GENERAL_LASTUP = "gl"
    NOVELTYPE = "nt"
    END = "e"
    GENERAL_ALL_NO = "ga"
    LENGTH = "l"
    TIME = "ti"
    ISSTOP = "i"
    ISR15 = "ir"
    ISBL = "ibl"
    ISGL = "igl"
    ISZANKOKU = "izk"
    ISTENSEI = "its"
    ISTENNI = "iti"
    GLOBAL_POINT = "gp"
    DAILY_POINT = "dp"
    WEEKLY_POINT = "wp"
    MONTHLY_POINT = "mp"
    QUARTER_POINT = "qp"
    YEARLY_POINT = "yp"
    FAV_NOVEL_CNT = "f"
    IMPRESSION_CNT = "imp"
    REVIEW_CNT = "r"
    ALL_POINT = "a"
    ALL_HYOKA_CNT = "ah"
    SASIE_CNT = "sa"
    KAIWARITU = "ka"
    NOVELUPDATED_AT = "nu"
    UPDATED_AT = "ua"
