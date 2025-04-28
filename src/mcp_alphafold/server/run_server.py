import argparse

from mcp.server.fastmcp.utilities.logging import get_logger

logger = get_logger(__name__)


def main():
    parser = argparse.ArgumentParser(description="mcp-server-alphafold")
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse"],
        default="sse",
        help="Transport mode: 'stdio' for standard IO or 'sse' for Server-Sent Events",
    )
    args = parser.parse_args()

    # Import is done here to make sure environment variables are loaded
    # only after we make the changes.
    from mcp_alphafold.server.mcp_server import create_server

    logger.info(f"Starting server with {args.transport} transport mode")
    app = create_server()
    app.run(transport=args.transport)


if __name__ == "__main__":
    main()
