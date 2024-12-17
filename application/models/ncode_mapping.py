"""ncode_mappingテーブル."""

import uuid

from sqlalchemy import TIMESTAMP, UUID, Column, String, UniqueConstraint, func

from models.base import Base


class NcodeMapping(Base):
    """IDとncodeのマッピングテーブル."""

    __tablename__ = "ncode_mapping"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
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
