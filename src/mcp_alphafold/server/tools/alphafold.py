import json
from typing import Any, Dict, List, Optional, Union

from mcp.server.fastmcp import FastMCP

from mcp_alphafold.server.tools.models import (
    AnnotationResponse,
    EntrySummaryResponse,
    UniprotSummaryResponse,
)
from mcp_alphafold.utils.http_util import request_api
from mcp_alphafold.server.tools.utils import with_docstring


BASE_URL = "https://alphafold.ebi.ac.uk/api"


def alphafold_tools(mcp: FastMCP):
    """Add AlphaFold tools to the MCP server."""
    tools = [
        get_alphafold_prediction, 
        get_uniprot_summary,
        get_annotations,
    ]
    for tool in tools:
        mcp.add_tool(tool)


@with_docstring("alphafold_prediction.md")
async def get_alphafold_prediction(
    qualifier: str,
    sequence_checksum: Optional[str] = None,
    output_json: bool = True,
) -> Union[str, Dict[str, Any]]:  # type: ignore[return-value]
    """
    Get all AlphaFold models for a UniProt accession.
    Args:
        qualifier (str): UniProt accession (e.g., 'Q5VSL9')
        sequence_checksum (str, optional): CRC64 checksum of the UniProt sequence

    Returns:
        Union[str, Dict[str, Any]]:
            - If output_json=True: JSON string
            - If output_json=False: List of entries or error dictionary
    """
    url = f"{BASE_URL}/prediction/{qualifier}"
    response, error = await request_api(
        url=url,
        method="GET",
        response_model_type=EntrySummaryResponse,
    )
    data: Union[List[Any], Dict[str, Any]]  # Add type annotation for data
    if response:
        data = [entry.model_dump_json(exclude_none=True) for entry in response.root]
    else:
        error_msg = f"Error {error.code if error else 'Unknown'}: {error.message if error else 'Unknown error'}"
        data = {"error": error_msg}

    return json.dumps(data) if output_json else data  # type: ignore


@with_docstring("uniprot_summary.md")
async def get_uniprot_summary(
    qualifier: str,
    output_json: bool = True,
) -> Union[str, Dict[str, Any]]:
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
    )

    if response:
        data = response.model_dump_json(exclude_none=True)
    else:
        error_msg = f"Error {error.code if error else 'Unknown'}: {error.message if error else 'Unknown error'}"
        data = {"error": error_msg}

    return json.dumps(data) if output_json else data


@with_docstring("uniprot_annotations.md")
async def get_annotations(
    qualifier: str,
    annotation_type: str = "MUTAGEN",
    output_json: bool = True,
) -> Union[str, Dict[str, Any]]:
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
    )
    if response:
        data = response.model_dump_json(exclude_none=True)
    else:
        error_msg = f"Error {error.code if error else 'Unknown'}: {error.message if error else 'Unknown error'}"
        data = {"error": error_msg}

    return json.dumps(data) if output_json else data
