"""Connection handling for MCP servers."""

from abc import ABC, abstractmethod
from contextlib import AsyncExitStack
from typing import Any, Dict, List

from mcp import ClientSession, StdioServerParameters
from mcp.client.sse import sse_client
from mcp.client.stdio import stdio_client


class MCPConnection(ABC):
    """Base class for MCP connection."""
    def __init__(self):
        self.session = None
        self._rw_ctx = None
        self._session_ctx = None
    
    @abstractmethod
    async def _create_rw_context(self):
        """Create read/write context based on the connection type."""
    
    async def __aenter__(self):
        """Initialize MCP server connection."""
        self._rw_ctx = await self._create_rw_context()
        read_write = await self._rw_ctx.__aenter__()
        read, write = read_write
        self._session_ctx = ClientSession(read, write)
        self.session = await self._session_ctx.__aenter__()
        await self.session.initialize()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Clean up MCP server connection resources."""
        try:
            if self._session_ctx:
                await self._session_ctx.__aexit__(exc_type, exc_val, exc_tb)
            if self._rw_ctx:
                await self._rw_ctx.__aexit__(exc_type, exc_val, exc_tb)
        except Exception as e:
            print(f"Error cleaning up MCP connection: {e}")
        finally:
            self.session = None
            self._session_ctx = None
            self._rw_ctx = None
    
    async def list_tools(self) -> Any:
        """Retrieve available tools from the MCP server."""
        response = await self.session.list_tools()
        return response.tools
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Call a tool on MCP server with the given arguments."""
        return await self.session.call_tool(tool_name, arguments)


class MCPConnectionStdio(MCPConnection):
    """MCP connection using standard input/output."""
    def __init__(self, command: str, args: List[str] = [], env: Dict[str, str] = None):
        super().__init__()
        self.command = command
        self.args = args 
        self.env = env
    
    async def _create_rw_context(self):
        return stdio_client(
            StdioServerParameters(
                command=self.command, args=self.args, env=self.env
            )
        )
    

class MCPConnectionSSE(MCPConnection):
    """MCP connection using Server-Sent Events."""
    def __init__(self, url: str, headers: Dict[str, str] = None):
        super().__init__()
        self.url = url 
        self.headers = headers 
    
    async def _create_rw_context(self):
        return sse_client(url=self.url, headers=self.headers)
    

def create_mcp_connection(config: Dict[str, Any]) -> MCPConnection:
    """Factory function to create the appropriate MCP connection."""
    conn_type = config.get("type", "stdio").lower()
    if conn_type == "stdio":
        if not config.get("command"):
            raise ValueError("Command is required for stdio connection.")
        return MCPConnectionStdio(
            command=config["command"], 
            args=config.get("args"),
            env=config.get("env"),
        )
    elif conn_type == "sse":
        if not config.get("url"):
            raise ValueError("URL is required for SSE connection.")
        return MCPConnectionSSE(
            url=config["url"],
            headers=config.get("headers"),
        )
    else:
        raise ValueError(f"Unsupported connection type: {conn_type}")
    

async def setup_mcp_connection(
        mcp_servers: List[Dict[str, Any]], 
        stack: AsyncExitStack,
) -> List[Any]:
    """Set up MCP server connections and create tool interfaces."""
    if not mcp_servers:
        return []
    mcp_tools = []
    for config in mcp_servers:
        try:
            connection = create_mcp_connection(config)
            await stack.enter_async_context(connection)
            tool_definitions = await connection.list_tools()
            return tool_definitions
        except Exception as e:
            print(f"Error setting up MCP server {config}: {e}")
    
    print(f"Loaded {len(tool_definitions)} MCP tools from {len(mcp_servers)} servers.")
