"""バッチで使用するデータ関連."""

from dataclasses import dataclass


@dataclass(frozen=True)
class NcodeMappingData:
    """ncodeのデータ."""

    id: str
    ncode: str
