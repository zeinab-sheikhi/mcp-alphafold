# import pytest

# from mcp_alphafold.server.mcp_server import server
# from mcp_alphafold.server.tools.alphafold import (
#     get_alpha_fold_prediction,
#     get_annotations,
#     get_uniprot_summary,
# )


# @pytest.mark.asyncio
# async def test_alphafold_prediction_tool(mocker):
#     # Test successful AlphaFold prediction
#     mock_response = {"entries": [{"entryId": "AF-P12345-F1"}]}
#     mock_get_prediction = mocker.patch(
#         "mcp_alphafold.server.tools.alphafold.get_alpha_fold_prediction",
#         return_value=mock_response,
#     )
#     # Get the tool from the server instance
#     tool = server.app.get_tool("alpha_fold_prediction_tool")
#     assert tool is not None

#     result = await tool.func(qualifier="P12345")

#     # verify function was called with correct parameters
#     mock_get_prediction.assert_called_once_with("P12345", None)
#     assert "AF-P12345-F1" in str(result)


# @pytest.mark.asyncio
# async def test_uniprot_summary_tool(mocker):
#     mock_response = {
#         "uniprot_entry": {
#             "ac": "P12345",
#             "id": "TEST_HUMAN",
#         },
#         "structures": [],
#     }
#     mock_get_summary = mocker.patch(
#         "mcp_alphafold.server.tools.mcp_server.get_uniprot_summary",
#         return_value=mock_response,
#     )
#     result = await get_uniprot_summary(qualifier="P12345")
#     mock_get_summary.assert_called_once_with("P12345")
#     assert isinstance(result, (str, dict))
#     assert "P12345" in str(result)


# @pytest.mark.asyncio
# async def test_annotations_tool(mocker):
#     mock_response = {
#         "accession": "P12345",
#         "id": "TEST_HUMAN",
#         "annotation": [
#             {
#                 "type": "MUTAGEN",
#                 "description": "Test annotation",
#             }
#         ],
#     }
#     mock_get_annotations = mocker.patch(
#         "mcp_alphafold.server.mcp_server.get_annotations",
#         return_value=mock_response,
#     )
#     result = await get_annotations(
#         qualifier="P12345",
#         annotation_type="MUTAGEN",
#     )
#     mock_get_annotations.assert_called_once_with("P12345", "MUTAGEN")
#     assert isinstance(result, (str, dict))
#     assert "P12345" in str(result)
