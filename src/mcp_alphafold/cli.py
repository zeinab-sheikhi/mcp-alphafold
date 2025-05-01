"""Command-line interface for the AlphaFold MCP server."""

import typer

from mcp_alphafold.server import AlphaFoldMCP
from mcp_alphafold.settings import settings

app = typer.Typer()


@app.command()
def run(
    transport: str = typer.Option(
        settings.TRANSPORT,
        help="Transport mode for MCP server",
        case_sensitive=False,
        show_choices=True,
        callback=lambda v: v if v in {"stdio", "sse"} else typer.BadParameter("Must be 'stdio' or 'sse'"),
    ),
    host: str = typer.Option(settings.SERVER_HOST, help="Host to bind the server to"),
    port: int = typer.Option(settings.SERVER_PORT, help="Port to bind the server to"),
    name: str = typer.Option(settings.SERVER_NAME, help="Name of the MCP server"),
) -> None:
    """Run the AlphaFold MCP server."""
    try:
        if transport not in {"stdio", "sse"}:
            raise typer.BadParameter("Must be 'stdio' or 'sse'")
        server = AlphaFoldMCP(
            name=name,
            host=host,
            port=port,
        )
        server.run(transport=transport)
    except Exception as e:
        print(f"Error: {e}")


def main():
    app()


if __name__ == "__main__":
    main()
