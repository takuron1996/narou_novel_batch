"""rankテーブル."""

from sqlalchemy import (
    UUID,
    Column,
    Date,
    ForeignKey,
    Integer,
    PrimaryKeyConstraint,
    String,
)

from models.base import Base
from models.ncode_mapping import NcodeMapping
from models.rank_type import RankType


class Rank(Base):
    """小説のランキングのテーブル."""

    __tablename__ = "rank"

    id = Column(UUID(as_uuid=True), ForeignKey(NcodeMapping.id), nullable=False)
    rank = Column(Integer, nullable=False)
    rank_date = Column(Date, nullable=False)
    rank_type = Column(String(1), ForeignKey(RankType.type), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint(
            "id", "rank", "rank_date", "rank_type", name="pk_rank"
        ),
    )
