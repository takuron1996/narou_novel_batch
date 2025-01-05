"""novel_keywordsテーブル."""

from sqlalchemy import Column, ForeignKey, PrimaryKeyConstraint, String
from sqlalchemy.dialects.postgresql import UUID

from models.base import Base
from models.keyword import Keyword
from models.ncode_mapping import NcodeMapping


class NovelKeywords(Base):
    """小説とキーワードの中間テーブル."""

    __tablename__ = "novel_keywords"
    id = Column(
        UUID(as_uuid=True),
        ForeignKey(NcodeMapping.id),
        nullable=False,
        comment="ID",
    )
    keyword_id = Column(
        String(43),
        ForeignKey(Keyword.keyword_id),
        nullable=False,
        comment="キーワードのID",
    )

    # 複合主キーの設定
    __table_args__ = (
        PrimaryKeyConstraint("id", "keyword_id", name="pk_novel_keywords"),
    )
