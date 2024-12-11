from sqlalchemy import (
    Column,
    String,
    Integer,
    Date,
    TIMESTAMP,
    func,
    ForeignKey,
    PrimaryKeyConstraint,
)
from models.base import Base
from models.ncode_mapping import NcodeMapping
from models.rank_type import RankType


class Rank(Base):
    """小説のランキングのテーブル"""

    __tablename__ = "rank"

    id = Column(String(36), ForeignKey(NcodeMapping.id), nullable=False)
    rank = Column(Integer, nullable=False)
    rank_date = Column(Date, nullable=False)
    rank_type = Column(String(1), ForeignKey(RankType.type), nullable=False)
    created_at = Column(
        TIMESTAMP, nullable=False, server_default=func.current_timestamp()
    )
    updated_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )
    deleted_at = Column(TIMESTAMP, nullable=True)

    __table_args__ = (
        PrimaryKeyConstraint(
            "id", "rank", "rank_date", "rank_type", name="pk_rank"
        ),
    )
