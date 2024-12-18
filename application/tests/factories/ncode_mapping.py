"""ncode_mappingのファクトリー関連."""

import uuid

import factory
from sqlalchemy.sql import func

from models.ncode_mapping import NcodeMapping


class NcodeMappingFactory(factory.alchemy.SQLAlchemyModelFactory):
    """ncode_mappingのファクトリークラス."""

    class Meta:
        """メタデータ."""

        model = NcodeMapping
        sqlalchemy_session = None  # セッションを初期化
        sqlalchemy_session_persistence = "commit"  # データをコミットする

    id = factory.LazyFunction(lambda: uuid.uuid4())
    ncode = factory.Sequence(lambda n: f"ncode_{n}")
    created_at = factory.LazyFunction(lambda: func.current_timestamp())
    updated_at = factory.LazyFunction(lambda: func.current_timestamp())
    deleted_at = None
