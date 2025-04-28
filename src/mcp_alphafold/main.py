import argparse


def main():
    """
    Main entry point for the mcp-server-alphafold script defined
    in pyproject.toml. It runs the MCP server with a specific transport
    protocol.
    """
    # Parse the command-line arguments to determine the transport protocol.
    parser = argparse.ArgumentParser(description="mcp-server-qdrant")
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse"],
        default="sse",
    )
    args = parser.parse_args()

    # Import is done here to make sure environment variables are loaded
    # only after we make the changes.
    from mcp_alphafold.server.mcp_server import create_server

    alphafold_mcp = create_server()
    alphafold_mcp.run(transport=args.transport)


if __name__ == "__main__":
    import sys

    sys.exit(main())
