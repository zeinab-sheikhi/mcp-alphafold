"""Command-line interface for the AlphaFold MCP server."""

import argparse
import sys
from typing import Optional


def parse_args(args: Optional[list[str]] = None) -> argparse.Namespace:
    """Parse command line arguments.

    Args:
        args: Command line arguments. If None, uses sys.argv[1:].

    Returns:
        Parsed arguments
    """

    parser = argparse.ArgumentParser(description="AlphaFold MCP server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse"],
        default="sse",
        help="Transport to use for MCP communication",
    )
    return parser.parse_args(args)


def main(args: Optional[list[str]] = None) -> None:
    """Run the MCP server.

    Args:
        args: Command line arguments. If None, uses sys.argv[1:].
    """

    parsed_args = parse_args(args)

    # Import is done here to make sure environment variables are loaded
    # only after we make the changes.
    from mcp_alphafold.server import AlphaFoldMCP

    try:
        mcp = AlphaFoldMCP()
        mcp.run(transport=parsed_args.transport)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
