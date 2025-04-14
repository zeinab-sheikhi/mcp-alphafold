import asyncio
import os
import streamlit as st
from mcp_client import MCPClient
from ui.chat import chat_ui


async def main():
    os.environ.pop("SSL_CERT_FILE", None)

    st.set_page_config(layout="wide")
    client = MCPClient()
    await client.connect("src/mcp_alphafold/mcp_server.py")

    try:
        await chat_ui(client)
    finally:
        await client.cleanup()
    
    
    # if len(sys.argv) < 2:
    #     print("Usage: python client.py <path_to_server_script>")
    #     sys.exit(1)
    
    # client = MCPClient()
    # try:
    #     await client.connect(sys.argv[1])
    #     await client.chat_loop()
    # finally:
    #     await client.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
    # sys.exit(0)
