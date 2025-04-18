import json
from typing import Any, Optional

from utils.http_util import request_api
from .models import (
    UniProtEntryResponse, 
    UniProtSearchParams,
)


BASE_URL = "https://rest.uniprot.org/uniprotkb"


async def search_uniprot(
    params: UniProtSearchParams, 
    output_json: bool = True,
) -> Optional[UniProtEntryResponse]:
    """
    Search UniProtKB entries based on a query.
    
    Args:
        params (UniProtParams): The parameters for the search query.

    Returns:
        UniProtSearchResponse: The search results, including the entries and metadata.
    """
    url = f"{BASE_URL}/search"
    response, error = await request_api(
        url,
        method="GET",
        request=params,
        tls_version=None,
        response_model_type=UniProtEntryResponse,
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
    
    return json.dumps(data) if output_json else data
