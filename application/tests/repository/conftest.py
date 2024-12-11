"""参考: https://tech.salesnow.jp/entry/pytest-with-clean-db"""

import pytest
from pytest_postgresql import factories
from pytest_postgresql import factories
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import NullPool
from models.base import Base
from sqlalchemy.engine.url import URL
from importlib import import_module
from pathlib import Path
from tests.factories.rank_type import RankTypeFactory
from tests.factories.ncode_mapping import NcodeMappingFactory
from tests.factories.rank import RankFactory


def import_migration_module(module):
    """マイグレーションに含めたいモジュールをimport."""
    for file_name in (p.name for p in Path(module).iterdir() if p.is_file()):
        if file_name in {"__init__.py", "base.py"}:
            continue
        file_name = file_name.replace(".py", "")
        import_module(f"{module}.{file_name}")


# Base.metadata.create_all(engine)はimportしていないとテーブルを作成しないため実施
import_migration_module("models")
postgresql_in_docker = factories.postgresql_noproc()
postgresql_fixture = factories.postgresql("postgresql_in_docker")


def init_db(db):
    """テスト用DBの初期設定"""
    # Factoryの初期設定
    RankTypeFactory._meta.sqlalchemy_session = db
    RankFactory._meta.sqlalchemy_session = db
    NcodeMappingFactory._meta.sqlalchemy_session = db

    # rank_type
    RankTypeFactory.create(type="d")
    RankTypeFactory.create(type="w")
    RankTypeFactory.create(type="m")
    RankTypeFactory.create(type="q")


@pytest.fixture
def db(postgresql_fixture):
    """テスト用DBセッションをSetupするFixture"""
    url = URL.create(
        drivername="postgresql",
        username=postgresql_fixture.info.user,
        password=postgresql_fixture.info.password,
        host=postgresql_fixture.info.host,
        database=postgresql_fixture.info.dbname,
        port=postgresql_fixture.info.port,
    )

    # engineを作成
    engine = create_engine(url, echo=False, poolclass=NullPool)

    # SQLAlchemyで定義しているテーブルを全て作成する
    Base.metadata.create_all(engine)
    SessionFactory = sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )

    # Sessionを生成
    db: Session = None
    try:
        db = SessionFactory()
        init_db(db)
        yield db
        db.commit()
    except Exception:
        db.rollback()
    finally:
        db.close()
