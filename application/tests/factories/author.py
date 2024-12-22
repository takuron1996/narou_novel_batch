"""authorのファクトリー関連."""

import uuid

import factory

from models.author import Author


class AuthorFactory(factory.alchemy.SQLAlchemyModelFactory):
    """authorのファクトリークラス."""

    class Meta:
        """メタデータ."""
        model = Author
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    author_id = factory.LazyFunction(lambda: uuid.uuid4())
    userid = factory.Sequence(lambda n: n + 1)
    writer = factory.Sequence(lambda n: f"name_{n}")
