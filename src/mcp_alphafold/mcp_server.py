from typing import Any, Dict, List, Optional, Union

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.utilities.logging import get_logger

from mcp_alphafold.tools.alphafold import (
    get_alpha_fold_prediction,
    get_annotations,
    get_uniprot_summary,
)
from mcp_alphafold.utils.tool_util import with_docstring

logger = get_logger("httpx")
logger.setLevel("WARN")

logger = get_logger(__name__)
logger.setLevel("INFO")


alphafold_mcp = FastMCP(
    name="AlphaFoldMCP",
    host="0.0.0.0",
    port=8050,
)


@with_docstring("alphafold_prediction.md")
@alphafold_mcp.tool()
async def alpha_fold_prediction_tool(
    qualifier: str,
    sequence_checksum: Optional[str] = None,
) -> Union[str, Dict[str, Any], List[Any]]:
    return await get_alpha_fold_prediction(qualifier, sequence_checksum)


@with_docstring("uniprot_summary.md")
@alphafold_mcp.tool()
async def uniprot_summary_tool(qualifier: str) -> Union[str, Dict[str, Any]]:
    return await get_uniprot_summary(qualifier)


@with_docstring("uniprot_annotations.md")
@alphafold_mcp.tool()
async def annotations_tool(
    qualifier: str,
    annotation_type: str = "MUTAGEN",
) -> Union[str, Dict[str, Any]]:
    return await get_annotations(qualifier, annotation_type)
