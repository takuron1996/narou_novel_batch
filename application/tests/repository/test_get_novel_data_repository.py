"""小説情報取得バッチのDB関連のテスト."""

import pytest

from repository.get_novel_data_repository import get_target_novel_data
from tests.factories.author import AuthorFactory
from tests.factories.ncode_mapping import NcodeMappingFactory
from tests.factories.novel import NovelFactory


@pytest.fixture
def novel_with_ncode_mapping():
    """
    Get novel data with its associated ncode mapping.
    
    Returns:
        NcodeMapping: A mapping object for novel with ncode 'N1121JW'
    """
    return NcodeMappingFactory.create(ncode="N1121JW")


@pytest.fixture
def novel_without_ncode_mapping():
    """
    Return a NcodeMapping object that is not linked to any novel in the novel table.
    
    Returns:
        NcodeMapping: A NcodeMapping instance with an empty space (" ") as ncode value
    """
    return NcodeMappingFactory.create(ncode=" ")


@pytest.fixture
def novel(novel_with_ncode_mapping):
    """
    Create a novel object with the given novel mapping data.
    
    Parameters:
        novel_with_ncode_mapping (NovelWithNcodeMapping): Novel mapping object containing novel metadata
    
    Returns:
        Novel: A novel object created with the specified ID and a generated author ID
    """
    return NovelFactory.create(
        id=novel_with_ncode_mapping.id, author_id=AuthorFactory().author_id
    )


# get_target_novel_data関連
def test_get_target_novel_data(db, novel_without_ncode_mapping, novel):
    """
    Test the get_target_novel_data function's behavior for novels without ncode mapping.
    
    Parameters:
        db: Database connection or session object
        novel_without_ncode_mapping (Novel): Novel object without ncode mapping
        novel (Novel): Standard novel object for comparison
    
    Assertions:
        - Verifies that exactly one result is returned
        - Confirms the returned result's ID matches the input novel's ID
        - Validates the returned ncode matches the input novel's ncode
    """
    results = get_target_novel_data(db)
    assert len(results) == 1
    assert results[0].get("id") == novel_without_ncode_mapping.id
    assert results[0].get("ncode") == novel_without_ncode_mapping.ncode
