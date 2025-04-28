import asyncio
import logging

from mcp_alphafold.client.mcp_client import MCPClient

logger = logging.getLogger(__name__)


async def run():
    # Create a stdio client
    client = MCPClient.stdio(
        command="python",
        args=["/Users/zeinab/projects/mcp-alphafold/src/mcp_alphafold/server/run_server.py", "--transport", "stdio"],
    )

    try:
        await client.connect()
        logger.info("Connected to MCP server successfully!")

        tools = await client.list_tools()
        logger.info("\nAvailable tools:", len(tools))

        result = await client.call_tool(
            tool_name="get_alphafold_prediction",
            qualifier="Q5VSL9",
        )
        logger.info("\nTool result:\n", result)

    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        # Always close the connection
        await client.cleanup()


def main():
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        logger.error("\nScript interrupted by user")
    except Exception as e:
        logger.error(f"Script error: {e}")


if __name__ == "__main__":
    main()
