"""rank_typeテーブル."""

from sqlalchemy import (
    Column,
    String,
)

from models.base import Base


class RankType(Base):
    """取得するランクの形式."""

    __tablename__ = "rank_type"

    type = Column(String(1), primary_key=True, nullable=False)
    period = Column(String(10), nullable=False)
