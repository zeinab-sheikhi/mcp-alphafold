from typing import Optional

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.utilities.logging import get_logger
from tools.alphafold import (
    get_alpha_fold_prediction,
    get_uniprot_summary,
    get_annotations,
)
from utils.tool_util import with_docstring


logger = get_logger("httpx")
logger.setLevel("WARN")

logger = get_logger(__name__)
logger.setLevel("INFO")

mcp_app = FastMCP(
    name="AlphaFoldMCP",
    host="0.0.0.0", 
    port=8050,
)


@with_docstring("alphafold_prediction.md")
@mcp_app.tool()
async def alpha_fold_prediction_tool(
    qualifier: str,
    sequence_checksum: Optional[str] = None,
) -> str:
    return await get_alpha_fold_prediction(qualifier, sequence_checksum)
    
@with_docstring("uniprot_summary.md")
@mcp_app.tool()
async def uniprot_summary_tool(qualifier: str) -> str:
    return await get_uniprot_summary(qualifier)


@with_docstring("uniprot_annotations.md")
@mcp_app.tool()
async def annotations_tool(
    qualifier: str,
    annotation_type: str = "MUTAGEN",
) -> str:
    return await get_annotations(qualifier, annotation_type)


async def start_server():
    """Run the MCP server with the STDIO transport."""
    
    try:
        await mcp_app.run(transport="sse")
        # await mcp_app.run_stdio_async()
        logger.info("MCP server stopped.")
        return 0
    except Exception as e:
        logger.error(f"Error running MCP server: {e}")
        return 1

if __name__ == "__main__":
    import asyncio
    asyncio.run(start_server())
