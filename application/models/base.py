"""DBのBase定義関連."""

from sqlalchemy import TIMESTAMP, Column, func
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """全てのmodelのベースとなるクラス."""

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
