from typing import Dict, List, Optional

from mcp_alphafold.client.base import SseMCPClient, StdioMCPClient

# from .chat_handler import ChatHandler


class MCPClient:
    @classmethod
    def stdio(
        cls,
        command: str,
        args: Optional[List[str]] = None,
        env: Optional[Dict[str, str]] = None,
    ) -> StdioMCPClient:
        "Create a stdio client."
        return StdioMCPClient(command, args, env)

    @classmethod
    def sse(
        cls,
        url: str,
        headers: Optional[Dict[str, str]] = None,
    ) -> SseMCPClient:
        "Create a SSE client."
        return SseMCPClient(url, headers)

    # @classmethod
    # async def create_chat_session(
    #     cls,
    #     client: BaseMCPClient,
    # ) -> ChatHandler:
    #     """Create a chat session with a client."""
    #     if not client.connection:
    #         await client.connect()
    #     return ChatHandler(client)
