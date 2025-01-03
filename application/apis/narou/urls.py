"""URL関連."""

from enum import Enum

from apis.narou.type import (
    NarouLimitType,
    NarouOfType,
    NarouOrderType,
    OutType,
    RankType,
)

# なろうAPI関連


class NarouParamsKey(Enum):
    """なろうAPI用のパラメータキー."""

    OUTPUT_FORMAT = "out"
    NCODE = "ncode"
    OF = "of"
    ORDER = "order"
    LIMIT = "lim"


class NarouURLBuilder:
    """なろうAPI用のURLビルダー."""

    def __init__(self):
        """初期化."""
        self._base_url = "https://api.syosetu.com/novelapi/api/"
        self._params = {}

    def set_output_format(self, out_type: OutType):
        """出力形式を設定する.

        Args:
            out_type (OutType): アウトタイプ

        Returns:
            NarouRankURLBuilder: 自身のインスタンス
        """
        self._params[NarouParamsKey.OUTPUT_FORMAT.value] = out_type.value
        return self

    def set_ncode(self, ncode: str):
        """ncodeを設定."""
        self._params[NarouParamsKey.NCODE.value] = ncode
        return self

    def set_of_list(self, of_list: list[NarouOfType]):
        """出力する項目を個別に指定."""
        self._params[NarouParamsKey.OF.value] = of_list
        return self

    def set_order(self, order: NarouOrderType):
        """出力順序を指定."""
        self._params[NarouParamsKey.ORDER.value] = order.value
        return self

    def set_limit(self, limit: int):
        """出力数を指定."""
        if limit < NarouLimitType.MIN_FETCH_LIMIT.value:
            limit = NarouLimitType.MIN_FETCH_LIMIT.value
        elif limit > NarouLimitType.MAX_FETCH_LIMIT.value:
            limit = NarouLimitType.MAX_FETCH_LIMIT.value
        self._params[NarouParamsKey.LIMIT.value] = limit
        return self

    def build(self) -> str:
        """クエリを組み立ててURLを生成."""
        out_put = self._params.get(NarouParamsKey.OUTPUT_FORMAT.value)
        if out_put is not None:
            out_put = f"{NarouParamsKey.OUTPUT_FORMAT.value}={out_put}"

        ncode = self._params.get(NarouParamsKey.NCODE.value)
        if ncode is not None:
            ncode = f"{NarouParamsKey.NCODE.value}={ncode}"

        of_list = self._params.get(NarouParamsKey.OF.value)
        of = None
        if of_list is not None:
            of = "-".join(tuple(map(lambda x: x.value, of_list)))
            of = f"{NarouParamsKey.OF.value}={of}"

        order = self._params.get(NarouParamsKey.ORDER.value)
        if order is not None:
            order = f"{NarouParamsKey.ORDER.value}={order}"

        limit = self._params.get(NarouParamsKey.LIMIT.value)
        if limit is not None:
            limit = f"{NarouParamsKey.LIMIT.value}={limit}"

        params = [
            x for x in (out_put, ncode, of, order, limit) if x is not None
        ]
        query = "&".join(params)
        return f"{self._base_url}?{query}"


# なろうランキングAPI関連
class NarouRankParamsKey(Enum):
    """なろうランキング用のパラメーターキー."""

    DATE = "date"
    RANK_TYPE = "rtype"
    OUTPUT_FORMAT = "out"


class NarouRankURLBuilder:
    """なろうランキング用のURLビルダー."""

    def __init__(self):
        """初期化."""
        self._base_url = "https://api.syosetu.com/rank/rankget/"
        self._params = {
            NarouRankParamsKey.OUTPUT_FORMAT.value: OutType.JSON.value
        }

    def set_date(self, rank_date: str):
        """日付を設定する。.

        Args:
            rank_date (str): 日付 (yyyymmdd形式)

        Returns:
            NarouRankURLBuilder: 自身のインスタンス
        """
        self._params[NarouRankParamsKey.DATE.value] = rank_date
        return self

    def set_rank_type(self, rank_type: RankType):
        """ランキングタイプを設定する。.

        Args:
            rank_type (RankType): ランキングタイプ

        Returns:
            NarouRankURLBuilder: 自身のインスタンス
        """
        self._params[NarouRankParamsKey.RANK_TYPE.value] = rank_type.value
        return self

    def set_output_format(self, out_type: OutType):
        """出力形式を設定する.

        Args:
            out_type (OutType): アウトタイプ

        Returns:
            NarouRankURLBuilder: 自身のインスタンス
        """
        self._params[NarouRankParamsKey.OUTPUT_FORMAT.value] = out_type.value
        return self

    def build(self) -> str:
        """URLを生成する。必須パラメータが設定されており、妥当性を検証する。.

        Returns:
            str: 生成されたURL

        Raises:
            ValueError: 必須パラメータが不足している場合や無効な値が設定されている場合
        """
        # 必須パラメータのチェック
        required_keys = (NarouRankParamsKey.DATE, NarouRankParamsKey.RANK_TYPE)
        missing_keys = [
            key.name for key in required_keys if key.value not in self._params
        ]

        if missing_keys:
            raise ValueError(
                f"必須パラメータが不足しています: {', '.join(missing_keys)}"
            )

        rank_date = self._params[NarouRankParamsKey.DATE.value]
        rank_type = RankType(self._params[NarouRankParamsKey.RANK_TYPE.value])

        # 日付とランキングタイプの妥当性を検証
        if not RankType.is_valid_date_for_rank_type(rank_type, rank_date):
            raise ValueError(
                f"日付 {rank_date} はランキングタイプ {rank_type.name} に対して無効です。"
            )

        # クエリを組み立ててURLを生成
        query = (
            f"{NarouRankParamsKey.RANK_TYPE.value}="
            f"{rank_date}-{rank_type.value}&"
            f"{NarouRankParamsKey.OUTPUT_FORMAT.value}={self._params[NarouRankParamsKey.OUTPUT_FORMAT.value]}"
        )
        return f"{self._base_url}?{query}"
