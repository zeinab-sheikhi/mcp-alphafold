from mcp.server.fastmcp import FastMCP

from mcp_alphafold.server.tools.alphafold import alphafold_tools
from mcp_alphafold.settings import settings


def create_server() -> FastMCP:
    """Create a new MCP server."""
    mcp_server = FastMCP(
        name=settings.SERVER_NAME,
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
    )

    alphafold_tools(mcp=mcp_server)

    return mcp_server
