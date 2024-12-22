"""genreテーブル."""

from sqlalchemy import Column, Integer, String

from models.base import Base


class Genre(Base):
    """ジャンルのテーブル."""

    __tablename__ = "genre"

    code = Column(
        Integer, primary_key=True, nullable=False, comment="ジャンルのコード"
    )
    name = Column(String(36), nullable=False, comment="ジャンル名")
