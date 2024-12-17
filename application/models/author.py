"""authorテーブル."""

import uuid

from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from models.base import Base


class Author(Base):
    """作者のテーブル."""

    __tablename__ = "author"
    author_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        comment="作者のID",
    )
    userid = Column(Integer, nullable=False, comment="作者のユーザーID(数値)")
    writer = Column(String(128), nullable=False, comment="作者名")
