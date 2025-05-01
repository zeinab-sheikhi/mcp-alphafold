"""Main entry point for the AlphaFold MCP server."""

import sys

from mcp_alphafold.cli import app


def main():
    try:
        app(standalone_mode=True)
    except SystemExit as e:
        sys.exit(e.code)


if __name__ == "__main__":
    main()

# Make main() the callable when importing __main__
__call__ = main
