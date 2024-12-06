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


class Rank(Base):
    """小説のランキングのテーブル"""

    __tablename__ = "rank"

    id = Column(String(26), ForeignKey(NcodeMapping.id), nullable=False)
    rank = Column(Integer, nullable=False)
    rank_date = Column(Date, nullable=False)
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
        PrimaryKeyConstraint("id", "rank", "rank_date", name="pk_rank"),
    )

    def __repr__(self):
        return (
            f"<Rank(id='{self.id}', rank='{self.rank}', rank_date='{self.rank_date}', "
            f"created_at='{self.created_at}', updated_at='{self.updated_at}', deleted_at='{self.deleted_at}')>"
        )
