"""小説情報取得バッチ関連のテスト."""

from batch.get_novel_data import NcodeMappingData, get_target_from_db


# get_target_from_db
def test_get_target_from_db(mocker):
    """
    Test the get_target_from_db function's retrieval of novel data from database.
    
    Parameters:
        mocker (pytest.MockFixture): Pytest fixture for mocking
    
    Returns:
        None
    
    Details:
        Mocks the get_target_novel_data function to return predefined novel entries
        and verifies that get_target_from_db correctly processes these entries into
        NcodeMappingData objects. Checks both the length of returned data and the
        exact content of the NcodeMappingData objects.
    
    Mock Data:
        - Two novel entries with id and ncode fields
        - First entry: id="d661e054-e78e-4bdc-8e0f-22c046063f5c", ncode="N1121JW"
        - Second entry: id="8e938824-9797-4e2c-bdbd-3e88e7df5b96", ncode="N0563JW"
    """
    mock_value = [
        {"id": "d661e054-e78e-4bdc-8e0f-22c046063f5c", "ncode": "N1121JW"},
        {"id": "8e938824-9797-4e2c-bdbd-3e88e7df5b96", "ncode": "N0563JW"},
    ]
    mocker.patch(
        "batch.get_novel_data.get_target_novel_data", return_value=mock_value
    )
    data_list = get_target_from_db()
    assert len(data_list) == 2
    assert data_list == [
        NcodeMappingData(
            id="d661e054-e78e-4bdc-8e0f-22c046063f5c", ncode="N1121JW"
        ),
        NcodeMappingData(
            id="8e938824-9797-4e2c-bdbd-3e88e7df5b96", ncode="N0563JW"
        ),
    ]
