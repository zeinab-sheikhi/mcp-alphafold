from .base import BaseMCPClient
from ..utils.connections import MCPConnectionSSE
from typing import Dict, Optional


class SSEMCPClient(BaseMCPClient):
    """MCP client using SSE connection."""
    def __init__(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
    ):
        super().__init__()
        self.url = url
        self.headers = headers or {}
    
    async def connect(self):
        """Connect to MCP server using SSE."""
        self.connection = MCPConnectionSSE(
            url=self.url, 
            headers=self.headers,
        )
        await self.stack.enter_async_context(self.connection)
