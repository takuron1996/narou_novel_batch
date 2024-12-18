"""keywordテーブル."""

import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from models.base import Base


class Keyword(Base):
    """キーワードのテーブル."""

    __tablename__ = "keyword"

    keyword_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        comment="キーワードのID",
    )
    name = Column(
        String(128), nullable=False, unique=True, comment="キーワード名"
    )
