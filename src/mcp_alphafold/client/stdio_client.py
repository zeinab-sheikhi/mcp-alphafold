from .base import BaseMCPClient
from ..utils.connections import MCPConnectionStdio
from typing import Dict, List, Optional


class StdioMCPClient(BaseMCPClient):
    """MCP client using standard input/output."""
    def __init__(
            self,
            command: str,
            args: Optional[List[str]] = None,
            env: Optional[Dict[str, str]] = None,
        ):
        super().__init__()
        self.command = command 
        self.args = args or []
        self.env = env or {}
    
    async def connect(self):
        """Connect to MCP server using stdio."""
        self.connection = MCPConnectionStdio(
            command=self.command,
            args=self.args,
            env=self.env,
        )
        await self.stack.enter_async_context(self.connection)


        



