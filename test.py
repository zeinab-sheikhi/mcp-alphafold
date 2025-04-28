import asyncio

from mcp_alphafold.client.mcp_client import MCPClient


async def main():
    # Create a stdio client
    client = MCPClient.stdio(
        command="python",
        args=["/Users/zeinab/projects/mcp-alphafold/src/mcp_alphafold/server/run_server.py", "--transport", "stdio"],
        # env={"PYTHONPATH": "/Users/zeinab/projects/mcp-alphafold"}
    )

    try:
        # Connect to the server
        await client.connect()
        print("Connected to MCP server successfully!")

        # List available tools
        tools = await client.list_tools()
        print("\nAvailable tools:")
        print(tools)
        # for tool in tools:
        #     print(f"- {tool.name}: {tool.description}")

        # # Example: Call the AlphaFold prediction tool
        # result = await client.call_tool(
        #     "alpha_fold_prediction_tool",
        #     {
        #         "qualifier": "P12345"  # Example UniProt ID
        #     }
        # )
        # print("\nTool result:", result)

    except Exception as e:
        print(f"Error: {e}")
    # finally:
    #     # Always close the connection
    #     await client.disconnect()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nScript interrupted by user")
    except Exception as e:
        print(f"Script error: {e}")
