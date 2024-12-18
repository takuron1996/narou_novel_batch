"""genreテーブル."""

from sqlalchemy import Column, ForeignKey, Integer, String

from models.base import Base


class Genre(Base):
    """ジャンルのテーブル."""

    __tablename__ = "genre"

    code = Column(
        Integer, primary_key=True, nullable=False, comment="ジャンルのコード"
    )
    name = Column(String(36), nullable=False, comment="ジャンル名")
    biggenre_code = Column(
        Integer,
        ForeignKey("biggenre.code"),
        nullable=False,
        comment="大ジャンルのコード",
    )
