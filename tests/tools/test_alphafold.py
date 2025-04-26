import pytest

from mcp_alphafold.tools.alphafold import get_alpha_fold_prediction
from mcp_alphafold.tools.models import EntrySummary, EntrySummaryResponse


@pytest.mark.asyncio
async def test_get_alphafold_prediction_success(mocker):
    mock_response = EntrySummaryResponse(
        root=[
            EntrySummary(
                entryId="some_id",
                uniprotAccession="P12345",
                uniprotId="P12345",
                uniprotDescription="Description of the protein",
                taxId="9606",
                organismScientificName="Homo sapiens",
                uniprotStart=1,
                uniprotEnd=100,
                uniprotSequence="MKTAYIAKQRQISFVKSHFSRYAEHHHFAADHSF",
                modelCreatedDate="2021-07-01",
                latestVersion="1.0",
                allVersions=[1, 2],
                bcifUrl="http://example.com/bcif",
                cifUrl="http://example.com/cif",
                pdbUrl="http://example.com/pdb",
                paeImageUrl="http://example.com/pae_image",
                paeDocUrl="http://example.com/pae_doc",
            )
        ]
    )
    mock_error = None

    mock_request_api = mocker.patch(
        "mcp_alphafold.utils.http_util.request_api",
        return_value=(mock_response, mock_error),
    )

    result = await get_alpha_fold_prediction("P12345", output_json=True)
    assert isinstance(result, str)
    assert "P12345" in result


@pytest.mark.asyncio
async def test_get_alphafold_prediction_failure(mocker):
    pass
