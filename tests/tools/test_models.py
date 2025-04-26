import pytest

from mcp_alphafold.tools.models import (
    Annotation,
    AnnotationResponse,
    AnnotationType,
    EntrySummary,
    EntrySummaryResponse,
    ModelCategory,
    ModelFormat,
    Region,
    UniprotEntry,
)
from mcp_alphafold.utils.http_util import RequestError


def test_entry_summary_model():
    """Test EntrySummary model validation"""
    # Test valid data
    valid_data = {
        "entryId": "AF-P12345-F1",
        "uniprotAccession": "P12345",
        "uniprotId": "TEST_HUMAN",
        "uniprotDescription": "Test protein",
        "taxId": 9606,
        "organismScientificName": "Homo sapiens",
        "uniprotStart": 1,
        "uniprotEnd": 100,
        "uniprotSequence": "MVKVGVNG",
        "modelCreatedDate": "2024-03-21",
        "latestVersion": 1,
        "allVersions": [1],
        "bcifUrl": "https://example.com/bcif",
        "cifUrl": "https://example.com/cif",
        "pdbUrl": "https://example.com/pdb",
        "paeImageUrl": "https://example.com/pae.png",
        "paeDocUrl": "https://example.com/pae.json",
    }

    entry = EntrySummary(**valid_data)
    assert entry.entryId == "AF-P12345-F1"
    assert entry.uniprotAccession == "P12345"
    assert entry.taxId == 9606
    assert entry.gene is None  # Optional field

    # Test invalid data
    with pytest.raises(ValueError):
        EntrySummary(
            **{**valid_data, "taxId": "invalid"}  # taxId should be int
        )

    # Test list response
    response = EntrySummaryResponse(root=[entry])
    assert len(response.root) == 1
    assert response.root[0].entryId == "AF-P12345-F1"


def test_uniprot_entry_model():
    """Test UniprotEntry model validation"""
    valid_data = {
        "ac": "P12345",
        "id": "TEST_HUMAN",
        "uniprot_checksum": "ABCD1234",
        "sequence_length": 100,
        "segment_start": 1,
        "segment_end": 100,
    }

    entry = UniprotEntry(**valid_data)
    assert entry.ac == "P12345"
    assert entry.sequence_length == 100

    # Test optional fields
    minimal_data = {"ac": "P12345"}
    entry = UniprotEntry(**minimal_data)
    assert entry.ac == "P12345"
    assert entry.id is None


def test_region_model():
    """Test Region model validation"""
    valid_data = {"start": 1, "end": 10, "annotation_value": [0.1, 0.2, 0.3], "unit": "score"}

    region = Region(**valid_data)
    assert region.start == 1
    assert region.end == 10
    assert len(region.annotation_value) == 3

    # Test without optional fields
    minimal_data = {"start": 1, "end": 10}
    region = Region(**minimal_data)
    assert region.annotation_value is None
    assert region.unit is None

    # Test invalid data
    with pytest.raises(ValueError):
        Region(start="invalid", end=10)  # start should be int


def test_annotation_model():
    """Test Annotation model validation"""
    valid_data = {
        "type": "MUTAGEN",
        "description": "Test annotation",
        "source_name": "AlphaMissense",
        "evidence": "Computational",
        "residues": [1, 2, 3],
        "regions": [{"start": 1, "end": 10}, {"start": 20, "end": 30}],
    }

    annotation = Annotation(**valid_data)
    assert annotation.type == AnnotationType.MUTAGEN
    assert len(annotation.regions) == 2
    assert annotation.source_url is None  # Optional field

    # Test without optional fields
    minimal_data = {
        "type": "MUTAGEN",
        "description": "Test annotation",
        "source_name": "AlphaMissense",
        "evidence": "Computational",
    }
    annotation = Annotation(**minimal_data)
    assert annotation.residues is None
    assert annotation.regions is None


def test_annotation_response_model():
    """Test AnnotationResponse model validation"""
    valid_data = {
        "accession": "P12345",
        "id": "TEST_HUMAN",
        "sequence": "MVKVGVNG",
        "annotation": [
            {
                "type": "MUTAGEN",
                "description": "Test annotation",
                "source_name": "AlphaMissense",
                "evidence": "Computational",
                "regions": [{"start": 1, "end": 10}],
            }
        ],
    }

    response = AnnotationResponse(**valid_data)
    assert response.accession == "P12345"
    assert len(response.annotation) == 1
    assert response.annotation[0].type == AnnotationType.MUTAGEN


def test_request_error_model():
    """Test RequestError model validation"""
    error = RequestError(code=404, message="Not found")
    assert error.code == 404
    assert error.message == "Not found"

    # Test with invalid data
    with pytest.raises(ValueError):
        RequestError(code="invalid", message="Error")  # code should be int


def test_model_enums():
    """Test enum values"""
    assert AnnotationType.MUTAGEN.value == "MUTAGEN"
    assert ModelFormat.PDB.value == "PDB"
    assert ModelFormat.MMCIF.value == "MMCIF"
    assert ModelFormat.BCIF.value == "BCIF"
    assert ModelCategory.EXPERIMENTALLY_DETERMINED.value == "EXPERIMENTALLY DETERMINED"
    assert ModelCategory.TEMPLATE_BASED.value == "TEMPLATE-BASED"
    assert ModelCategory.AB_INITIO.value == "AB-INITIO"
    assert ModelCategory.CONFORMATIONAL_ENSEMBLE.value == "CONFORMATIONAL ENSEMBLE"
