"""biggenreテーブル."""

from sqlalchemy import Column, Integer, String

from models.base import Base


class BigGenre(Base):
    """大ジャンルのテーブル."""

    __tablename__ = "biggenre"

    code = Column(
        Integer, primary_key=True, nullable=False, comment="大ジャンルのコード"
    )
    name = Column(String(36), nullable=False, comment="大ジャンル名")
