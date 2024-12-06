from sqlalchemy import Column, String, TIMESTAMP, func, UniqueConstraint
from models.base import Base
import uuid


class NcodeMapping(Base):
    """IDとncodeのマッピングテーブル"""

    __tablename__ = "ncode_mapping"

    id = Column(String(26), primary_key=True, default=lambda: str(uuid.uuid4()))
    ncode = Column(String(255), nullable=False, unique=True)
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

    __table_args__ = (UniqueConstraint("ncode", name="uq_ncode"),)

    def __repr__(self):
        return f"<NcodeMapping(id='{self.id}', ncode='{self.ncode}', created_at='{self.created_at}', updated_at='{self.updated_at}', deleted_at='{self.deleted_at}')>"
