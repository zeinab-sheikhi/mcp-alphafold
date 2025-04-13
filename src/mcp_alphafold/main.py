import asyncio
import sys
import os
from mcp_client import MCPClient


async def main():
    os.environ.pop("SSL_CERT_FILE", None)

    if len(sys.argv) < 2:
        print("Usage: python client.py <path_to_server_script>")
        sys.exit(1)
    
    client = MCPClient()
    try:
        await client.connect(sys.argv[1])
        await client.chat_loop()
    finally:
        await client.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
    sys.exit(0)
