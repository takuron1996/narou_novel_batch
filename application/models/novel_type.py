"""novel_typeテーブル."""

from sqlalchemy import Column, Integer, String

from models.base import Base


class NovelType(Base):
    """ノベルの形式のテーブル."""

    __tablename__ = "novel_type"

    code = Column(
        Integer,
        primary_key=True,
        nullable=False,
        comment="ノベルの形式のコード",
    )
    name = Column(String(2), nullable=False, comment="ノベルの形式名")
