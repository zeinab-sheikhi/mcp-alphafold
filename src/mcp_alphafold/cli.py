"""Command-line interface for the AlphaFold MCP server."""

from typing import Optional

import typer

from mcp_alphafold.server import AlphaFoldMCP
from mcp_alphafold.settings import settings

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
        server.run(
            host=host or settings.SERVER_HOST,
            port=port or settings.SERVER_PORT,
            transport=transport or settings.TRANSPORT,
        )
    except Exception as e:
        print(f"Error: {e}")
