from mcp.server.fastmcp import FastMCP

from mcp_alphafold.tools.alphafold import alphafold_tools
from mcp_alphafold.settings import settings


def create_server() -> FastMCP:
    """Create a new MCP server."""
    app = FastMCP(
        name=settings.SERVER_NAME,
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
    )

    alphafold_tools(mcp=app)

    return app
