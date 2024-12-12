"""URL関連."""

from enum import Enum

from apis.narou.type import OutType, RankType


class ParamsKey(Enum):
    """なろうランキング用のパラメーターキー."""
    DATE = "date"
    RANK_TYPE = "rtype"
    OUTPUT_FORMAT = "out"


class NarouRankURLBuilder:
    """なろうランキング用のURLビルダー."""

    def __init__(self):
        """初期化."""
        self._base_url = "https://api.syosetu.com/rank/rankget/"
        self._params = {ParamsKey.OUTPUT_FORMAT.value: OutType.JSON.value}

    def set_date(self, rank_date: str):
        """日付を設定する。.

        Args:
            rank_date (str): 日付 (yyyymmdd形式)

        Returns:
            NarouRankURLBuilder: 自身のインスタンス
        """
        self._params[ParamsKey.DATE.value] = rank_date
        return self

    def set_rank_type(self, rank_type: RankType):
        """ランキングタイプを設定する。.

        Args:
            rank_type (RankType): ランキングタイプ

        Returns:
            NarouRankURLBuilder: 自身のインスタンス
        """
        self._params[ParamsKey.RANK_TYPE.value] = rank_type.value
        return self

    def set_output_format(self, out_type: OutType):
        """出力形式を設定する.

        Args:
            out_type (OutType): アウトタイプ

        Returns:
            NarouRankURLBuilder: 自身のインスタンス
        """
        self._params[ParamsKey.OUTPUT_FORMAT.value] = out_type.value
        return self

    def build(self) -> str:
        """URLを生成する。必須パラメータが設定されており、妥当性を検証する。.

        Returns:
            str: 生成されたURL

        Raises:
            ValueError: 必須パラメータが不足している場合や無効な値が設定されている場合
        """
        # 必須パラメータのチェック
        required_keys = (ParamsKey.DATE, ParamsKey.RANK_TYPE)
        missing_keys = [
            key.name for key in required_keys if key.value not in self._params
        ]

        if missing_keys:
            raise ValueError(
                f"必須パラメータが不足しています: {', '.join(missing_keys)}"
            )

        rank_date = self._params[ParamsKey.DATE.value]
        rank_type = RankType(self._params[ParamsKey.RANK_TYPE.value])

        # 日付とランキングタイプの妥当性を検証
        if not RankType.is_valid_date_for_rank_type(rank_type, rank_date):
            raise ValueError(
                f"日付 {rank_date} はランキングタイプ {rank_type.name} に対して無効です。"
            )

        # クエリを組み立ててURLを生成
        query = (f"{ParamsKey.RANK_TYPE.value}="
                 f"{rank_date}-{rank_type.value}&"
                 f"{ParamsKey.OUTPUT_FORMAT.value}={self._params[ParamsKey.OUTPUT_FORMAT.value]}")
        return f"{self._base_url}?{query}"
