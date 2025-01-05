"""authorのファクトリー関連."""

import factory

from models.author import Author, get_author_id


class AuthorFactory(factory.alchemy.SQLAlchemyModelFactory):
    """authorのファクトリークラス."""

    class Meta:
        """メタデータ."""

        model = Author
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    author_id = factory.LazyFunction(lambda: get_author_id())
    userid = factory.Sequence(lambda n: n + 1)
    writer = factory.Sequence(lambda n: f"name_{n}")
