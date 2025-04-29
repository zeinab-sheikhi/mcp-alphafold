import asyncio
import logging

from mcp_alphafold.client.mcp_client import MCPClient

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


async def run_client():
    client = MCPClient.stdio(
        command="python",
        args=[
            "/Users/zsheikhitarghi/projects/mcp-alphafold/src/mcp_alphafold/server/run_server.py",
            "--transport",
            "stdio",
        ],
    )

    try:
        await client.connect()
        logger.info("Connected to MCP server successfully!")

        tools = await client.list_tools()
        logger.info(f"Available tools: {len(tools)}")

        result = await client.call_tool(
            tool_name="get_alphafold_prediction",
            qualifier="Q5VSL9",
        )
        logger.info(f"Tool result:\n{result.content[0].text}")
        await asyncio.sleep(5)

    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        await client.cleanup()


def main():
    try:
        asyncio.run(run_client())
    except KeyboardInterrupt:
        logger.error("Script interrupted by user")
    except Exception as e:
        logger.error(f"Script error: {e}")


if __name__ == "__main__":
    main()
