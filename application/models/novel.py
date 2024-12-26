"""novelテーブル."""

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from models.author import Author
from models.base import Base
from models.biggenre import BigGenre
from models.genre import Genre
from models.ncode_mapping import NcodeMapping
from models.novel_type import NovelType


class Novel(Base):
    """小説テーブル."""

    __tablename__ = "novel"

    id = Column(
        UUID(as_uuid=True),
        ForeignKey(NcodeMapping.id),
        primary_key=True,
        nullable=False,
        comment="ID",
    )
    author_id = Column(
        String(42),
        ForeignKey(Author.author_id),
        nullable=False,
        comment="作者のID",
    )
    title = Column(String(128), nullable=False, comment="作品名")
    biggenre_code = Column(
        Integer,
        ForeignKey(BigGenre.code),
        nullable=False,
        comment="大ジャンルのコード",
    )
    genre_code = Column(
        Integer,
        ForeignKey(Genre.code),
        nullable=False,
        comment="ジャンルのコード",
    )
    novel_type_id = Column(
        Integer,
        ForeignKey(NovelType.code),
        nullable=False,
        comment="ノベルの形式のコード",
    )
    # 各種フラグ (R15、BL、GL、残酷、異世界転生、異世界転移)
    isr15 = Column(
        Boolean,
        nullable=False,
        default=False,
        comment="「R15」が含まれるかどうか",
    )
    isbl = Column(
        Boolean,
        nullable=False,
        default=False,
        comment="「ボーイズラブ」が含まれるかどうか",
    )
    isgl = Column(
        Boolean,
        nullable=False,
        default=False,
        comment="「ガールズラブ」が含まれるかどうか",
    )
    iszankoku = Column(
        Boolean,
        nullable=False,
        default=False,
        comment="「残酷な描写あり」が含まれるかどうか",
    )
    istensei = Column(
        Boolean,
        nullable=False,
        default=False,
        comment="「異世界転生」が含まれるかどうか",
    )
    istenni = Column(
        Boolean,
        nullable=False,
        default=False,
        comment="「異世界転移」が含まれるかどうか",
    )
