import pytest

from mcp_alphafold.server.mcp_server import (
    alpha_fold_prediction_tool,
    annotations_tool,
    uniprot_summary_tool,
)


@pytest.mark.asyncio
async def test_alphafold_prediction_tool(mocker):
    # Test successful AlphaFold prediction
    mock_response = {"entries": [{"entryId": "AF-P12345-F1"}]}
    mock_get_prediction = mocker.patch(
        "mcp_alphafold.mcp_server.get_alpha_fold_prediction",
        return_value=mock_response,
    )
    result = await alpha_fold_prediction_tool(
        qualifier="P12345",
        sequence_checksum="ABC123",
    )
    # verify function was called with correct parameters
    mock_get_prediction.assert_called_once_with("P12345", "ABC123")
    assert isinstance(result, (str, dict, list))
    assert "AF-P12345-F1" in str(result)


@pytest.mark.asyncio
async def test_uniprot_summary_tool(mocker):
    mock_response = {
        "uniprot_entry": {
            "ac": "P12345",
            "id": "TEST_HUMAN",
        },
        "structures": [],
    }
    mock_get_summary = mocker.patch(
        "mcp_alphafold.mcp_server.get_uniprot_summary",
        return_value=mock_response,
    )
    result = await uniprot_summary_tool(qualifier="P12345")
    mock_get_summary.assert_called_once_with("P12345")
    assert isinstance(result, (str, dict))
    assert "P12345" in str(result)


@pytest.mark.asyncio
async def test_annotations_tool(mocker):
    mock_response = {
        "accession": "P12345",
        "id": "TEST_HUMAN",
        "annotation": [
            {
                "type": "MUTAGEN",
                "description": "Test annotation",
            }
        ],
    }
    mock_get_annotations = mocker.patch(
        "mcp_alphafold.mcp_server.get_annotations",
        return_value=mock_response,
    )
    result = await annotations_tool(
        qualifier="P12345",
        annotation_type="MUTAGEN",
    )
    mock_get_annotations.assert_called_once_with("P12345", "MUTAGEN")
    assert isinstance(result, (str, dict))
    assert "P12345" in str(result)
