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
        default="stdio",
    )
    args = parser.parse_args()

    # Import is done here to make sure environment variables are loaded
    # only after we make the changes.
    from mcp_alphafold.mcp_server import alpahfold_mcp

    alpahfold_mcp.run(transport=args.transport)
