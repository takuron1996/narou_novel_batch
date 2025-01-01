"""keywordテーブル."""

import uuid

from sqlalchemy import Column, String

from models.base import Base


def get_keyword_id():
    """キーワードを一意に特定するIDを生成."""
    return f"KEYWORD{uuid.uuid4()}"


class Keyword(Base):
    """キーワードのテーブル."""

    __tablename__ = "keyword"

    keyword_id = Column(
        String(43),
        primary_key=True,
        default=get_keyword_id,
        nullable=False,
        comment="キーワードのID",
    )
    name = Column(
        String(128), nullable=False, unique=True, comment="キーワード名"
    )
