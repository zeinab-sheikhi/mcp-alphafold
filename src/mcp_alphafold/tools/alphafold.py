from typing import Any, List, Optional

from http_utils import request_api
from .models import (
    UniprotSummaryResponse,
    AnnotationResponse,
    EntrySummaryResponse,
    EntrySummary,
)


BASE_URL = "https://alphafold.ebi.ac.uk/api"


async def get_alpha_fold_prediction(
        qualifier: str,
        sequence_checksum: Optional[str] = None,
        output_json: bool = True,
) -> Optional[List[EntrySummary]]:
    """
    Get all AlphaFold models for a UniProt accession.
    Args:
        qualifier (str): UniProt accession (e.g., 'Q5VSL9')
        sequence_checksum (str, optional): CRC64 checksum of the UniProt sequence

    Returns:
        List[EntrySummary]: List of prediction metadata
    """
    url = f"{BASE_URL}/prediction/{qualifier}"
    response, error = await request_api(
        url=url,
        method="GET",
        tls_version=None,
        response_model_type=EntrySummaryResponse,
    )
        
    if response:
        data = [
            entry.model_dump_json(exclude_none=True)
            for entry in response.root
        ]
    else:
        data: list[dict[str, Any]] = [
            {"error": f"Error {error.code}: {error.message}"}
        ]
    
    return data


async def get_uniprot_summary(
        qualifier: str,
        output_json: bool = True,
) -> Optional[UniprotSummaryResponse]:
    """
    Get UniProt summary and structure information for a protein.

    Args:
        qualifier (str): UniProtKB accession number (AC), entry name (ID) 
                    or CRC64 checksum of the UniProt sequence

    Returns:
        Optional[UniprotSummaryResponse]: Complete response including UniProt entry and structures
    """
    url = f"{BASE_URL}/uniprot/summary/{qualifier}.json"
    
    response, error = await request_api(
        url=url,
        method="GET",
        response_model_type=UniprotSummaryResponse,
        tls_version=None,
    )
    
    if response:
        data = response.model_dump_json(exclude_none=True)
    else:
        data: list[dict[str, Any]] = [
            {"error": f"Error {error.code}: {error.message}"}
        ]
    
    return data
   

async def get_annotations(
        qualifier: str, 
        annotation_type: str = "MUTAGEN",
        output_json: bool = True,
) -> Optional[AnnotationResponse]:
    """
    Get all annotations for a UniProt residue range.

    Args:
        qualifier (str): UniProt accession
        annotation_type (str): Type of annotation (e.g., MUTAGEN for AlphaMissense)

    Returns:
        Optional[AnnotationResponse]: Annotation data including residue scores
    """
    url = f"{BASE_URL}/annotations/{qualifier}?annotation_type={annotation_type}"    
    
    response, error = await request_api(
        url=url,
        method="GET",
        response_model_type=AnnotationResponse,
        tls_version=None,
    )
    if response:
        data = response.model_dump_json(exclude_none=True)
    else:
        data: list[dict[str, Any]] = [
            {"error": f"Error {error.code}: {error.message}"}
        ]
    
    return data
