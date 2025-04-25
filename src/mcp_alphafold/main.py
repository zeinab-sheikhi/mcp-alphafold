import asyncio
from mcp_alphafold.mcp_server import alpahfold_mcp

# async def start_server():
#     """Run the MCP server with the STDIO transport."""
    
#     try:
#         await alpahfold_mcp.run(transport="sse")
#         # await mcp_app.run_stdio_async()
#         logger.info("MCP server stopped.")
#         return 0
#     except Exception as e:
#         logger.error(f"Error running MCP server: {e}")
#         return 1

# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(start_server())

def main():
    try:
        alpahfold_mcp.run(transport="sse")
    except Exception as e:
        print(f"Error running MCP server: {e}")


if __name__ == "__main__":
    main()
