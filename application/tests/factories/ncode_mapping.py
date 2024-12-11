import factory
from models.ncode_mapping import NcodeMapping
import uuid
from sqlalchemy.sql import func


class NcodeMappingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = NcodeMapping

    id = factory.LazyFunction(lambda: str(uuid.uuid4()))
    ncode = factory.Sequence(lambda n: f"ncode_{n}")
    created_at = factory.LazyFunction(lambda: func.current_timestamp())
    updated_at = factory.LazyFunction(lambda: func.current_timestamp())
    deleted_at = None