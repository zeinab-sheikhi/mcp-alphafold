from abc import ABC, abstractmethod
from contextlib import AsyncExitStack
from typing import Any, Dict, List, Optional

from anthropic import Anthropic
from dotenv import load_dotenv
from .mcp_connection import MCPConnectionSSE, MCPConnectionStdio

load_dotenv()


class BaseMCPClient(ABC):
    """Base class for MCP clients."""
    def __init__(self):
        self.stack = AsyncExitStack()
        self.connection = None
        self.model = "claude-3-5-sonnet-20240620"
        self.anthropic = Anthropic()
        self._tools = None
    
    @abstractmethod
    async def connect(self) -> None:
        """Establish connection to the MCP server."""
        raise NotImplementedError("Subclasses must implement this method.")
    
    async def list_tools(self) -> List[Dict[str, Any]]:
        """Get available tools from the server."""
        if not self.connection:
            raise RuntimeError("Not conncted to MCP server.")
        if not self._tools: 
            tools = await self.connection.list_tools()
            self._tools = [{
                "name": tool.name, 
                "description": tool.description, 
                "input_schema": tool.inputSchema, 
            } for tool in tools]
        
        return self._tools
    
    async def call_tool(self, tool_name: str, **kwargs) -> Any:
        """Call a specific tool with the provided parameters."""
        if not self.connection:
            raise RuntimeError("Not connected to MCP server.")
        return await self.connection.call_tool(tool_name, kwargs)
    
    async def cleanup(self) -> None:
        """Close the connection and clean up the resources."""
        await self.stack.aclose()
        self.connection = None
        self._tools = None
    
    async def __aenter__(self):
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.cleanup()


class SseMCPClient(BaseMCPClient):
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
