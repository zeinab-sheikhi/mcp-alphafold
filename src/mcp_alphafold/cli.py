"""Command-line interface for the AlphaFold MCP server."""

import logging
import sys
from typing import Literal, Optional, cast

import typer

from mcp_alphafold.server import AlphaFoldMCP
from mcp_alphafold.settings import settings

logger = logging.getLogger(__name__)
app = typer.Typer()
TransportType = Literal["stdio", "streamable-http"]


@app.command()
def run(
    host: Optional[str] = None,
    port: Optional[int] = None,
    name: Optional[str] = None,
    transport: Optional[TransportType] = None,
) -> None:
    """Run the AlphaFold MCP server."""
    host = typer.Option(host, help="Host to bind the server to")
    port = typer.Option(port, help="Port to bind the server to")
    name = typer.Option(name, help="Name of the MCP server")
    transport = typer.Option(transport, help="Transport mode for MCP server; can be 'stdio' or 'streamable-http'")

    try:
        server = AlphaFoldMCP(name=name or settings.SERVER_NAME)
        transport = transport or settings.TRANSPORT

        if transport == "stdio":
            # For stdio transport, only pass transport
            server.run(transport=cast(TransportType, transport))
        else:
            # For streamable-http transport, pass all arguments
            server.run(
                transport=cast(TransportType, transport),
                host=host or settings.SERVER_HOST,
                port=port or settings.SERVER_PORT,
            )
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        sys.exit(1)
