"""ncode_mappingテーブル."""

import uuid

from sqlalchemy import UUID, Column, String, UniqueConstraint

from models.base import Base


class NcodeMapping(Base):
    """IDとncodeのマッピングテーブル."""

    __tablename__ = "ncode_mapping"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ncode = Column(String(255), nullable=False, unique=True)

    __table_args__ = (UniqueConstraint("ncode", name="uq_ncode"),)
