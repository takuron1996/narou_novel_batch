"""authorテーブル."""

import uuid

from sqlalchemy import Column, Integer, String

from models.base import Base


def get_author_id():
    """作者を一意に特定するIDを生成."""
    return f"AUTH{uuid.uuid4()}"


class Author(Base):
    """作者のテーブル."""

    __tablename__ = "author"
    author_id = Column(
        String(42),
        primary_key=True,
        default=get_author_id,
        nullable=False,
        comment="作者のID",
    )
    userid = Column(
        Integer, nullable=False, unique=True, comment="作者のユーザーID(数値)"
    )
    writer = Column(String(128), nullable=False, comment="作者名")
