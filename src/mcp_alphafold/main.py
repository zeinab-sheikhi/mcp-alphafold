import asyncio
import os
from client.mcp_client import MCPClient


async def run_client():
    os.environ.pop("SSL_CERT_FILE", None)
    client = MCPClient.stdio(command="python", args=["src/mcp_alphafold/mcp_server.py"])
    chat_handler = await MCPClient.create_chat_session(client)
    print("Connected to MCP server...")
    while True:
        query = input("Enter your query or 'quit' to exit:\n")
        if query.lower() == "quit":
            break
        response = await chat_handler.process_query(query)
        print(response) 


def main():
    asyncio.run(run_client())


if __name__ == "__main__":
    main()
    # sys.exit(0)
