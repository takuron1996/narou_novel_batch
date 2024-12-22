"""小説情報取得バッチのDB関連のテスト."""

import pytest

from repository.get_novel_data_repository import get_target_novel_data
from tests.factories.author import AuthorFactory
from tests.factories.ncode_mapping import NcodeMappingFactory
from tests.factories.novel import NovelFactory


@pytest.fixture
def novel_with_ncode_mapping():
    """novelテーブルに格納されているデータと紐付くncode_mappingのデータ."""
    return NcodeMappingFactory.create(ncode="N1121JW")


@pytest.fixture
def novel_without_ncode_mapping():
    """novelテーブルに格納されているデータと紐付かないncode_mappingのデータ."""
    return NcodeMappingFactory.create(ncode=" ")


@pytest.fixture
def novel(novel_with_ncode_mapping):
    """novelデータ."""
    return NovelFactory.create(
        id=novel_with_ncode_mapping.id, author_id=AuthorFactory().author_id
    )


# get_target_novel_data関連
def test_get_target_novel_data(db, novel_without_ncode_mapping, novel):
    """テスト."""
    results = get_target_novel_data(db)
    assert len(results) == 1
    assert results[0].get("id") == novel_without_ncode_mapping.id
    assert results[0].get("ncode") == novel_without_ncode_mapping.ncode
