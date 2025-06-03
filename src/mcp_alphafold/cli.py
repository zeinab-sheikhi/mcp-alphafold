"""Command-line interface for the AlphaFold MCP server."""

import logging
import sys
from typing import Optional

import typer

from mcp_alphafold.server import AlphaFoldMCP
from mcp_alphafold.settings import settings

logger = logging.getLogger(__name__)

app = typer.Typer()


@app.command()
def run(
    host: Optional[str] = typer.Option(None, help="Host to bind the server to"),
    port: Optional[int] = typer.Option(None, help="Port to bind the server to"),
    name: Optional[str] = typer.Option(None, help="Name of the MCP server"),
    transport: Optional[str] = typer.Option(
        None, help="Transport mode for MCP server; can be 'stdio' or 'streamable-http'"
    ),
) -> None:
    """Run the AlphaFold MCP server."""
    try:
        server = AlphaFoldMCP(name=name or settings.SERVER_NAME)
        transport = transport or settings.TRANSPORT

        if transport == "stdio":
            server.run(transport=transport)
        else:
            server.run(
                host=host or settings.SERVER_HOST,
                port=port or settings.SERVER_PORT,
                transport=transport,
            )
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        sys.exit(1)
