import pytest

from mcp_alphafold.tools.alphafold import (
    get_alpha_fold_prediction,
    get_annotations,
    get_uniprot_summary,
)
from mcp_alphafold.tools.models import (
    Annotation,
    AnnotationResponse,
    AnnotationType,
    Entity,
    EntityPolyType,
    EntityType,
    EntrySummary,
    EntrySummaryResponse,
    IdentifierCategory,
    ModelCategory,
    ModelFormat,
    Region,
    Structure,
    StructureSummary,
    UniprotEntry,
    UniprotSummaryResponse,
)


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
async def test_get_uniprot_summary_success(mocker):
    mock_response = UniprotSummaryResponse(
        uniprot_entry=UniprotEntry(
            ac="P12345",
            id="TEST_HUMAN",
            uniprot_checksum="ABC123",
            sequence_length=100,
            segment_start=1,
            segment_end=100,
        ),
        structures=[
            Structure(
                summary=StructureSummary(
                    model_identifier="AF-P12345-F1",
                    model_category=ModelCategory.AB_INITIO,
                    model_url="https://example.com/model",
                    model_format=ModelFormat.MMCIF,
                    provider="AlphaFold DB",
                    created="2024-03-21",
                    sequence_identity=1.0,
                    uniprot_start=1,
                    uniprot_end=100,
                    coverage=1.0,
                    confidence_avg_local_score=80.5,
                    entities=[
                        Entity(
                            entity_type=EntityType.POLYMER,
                            entity_poly_type=EntityPolyType.POLYPEPTIDE_L,
                            identifier="P12345",
                            identifier_category=IdentifierCategory.UNIPROT,
                            description="Test protein",
                            chain_ids=["A"],
                        )
                    ],
                )
            )
        ],
    )
    mock_error = None
    mock_request_api = mocker.patch(
        "mcp_alphafold.utils.http_util.request_api",
        return_value=(mock_response, mock_error),
    )
    result = await get_uniprot_summary("P12345", output_json=True)
    assert isinstance(result, str)
    assert "P12345" in result


@pytest.mark.asyncio
async def test_get_annotations_success(mocker):
    """Test successful annotations retrieval"""
    mock_response = AnnotationResponse(
        accession="P12345",
        id="TEST_HUMAN",
        sequence="MVKVGVNG",
        annotation=[
            Annotation(
                type=AnnotationType.MUTAGEN,
                description="Test annotation",
                source_name="AlphaMissense",
                evidence="Computational",
                regions=[Region(start=1, end=10, annotation_value=[0.8, 0.9], unit="confidence")],
            )
        ],
    )
    mock_error = None

    mock_request_api = mocker.patch(
        "mcp_alphafold.utils.http_util.request_api",
        return_value=(mock_response, mock_error),
    )

    result = await get_annotations("P12345", annotation_type="MUTAGEN", output_json=True)
    assert isinstance(result, str)
