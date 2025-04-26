# """Connection handling for MCP servers."""

# from abc import ABC, abstractmethod
# from typing import Any, Dict, List, Optional

# from mcp import ClientSession, StdioServerParameters
# from mcp.client.sse import sse_client
# from mcp.client.stdio import stdio_client


# class MCPConnection(ABC):
#     """Base class for MCP connection."""

#     def __init__(self):
#         self.session = None
#         self._rw_ctx = None
#         self._session_ctx = None

#     @abstractmethod
#     async def _create_rw_context(self):
#         """Create read/write context based on the connection type."""

#     async def __aenter__(self):
#         """Initialize MCP server connection."""
#         self._rw_ctx = await self._create_rw_context()
#         read_write = await self._rw_ctx.__aenter__()
#         read, write = read_write
#         self._session_ctx = ClientSession(read, write)
#         self.session = await self._session_ctx.__aenter__()
#         await self.session.initialize()
#         return self

#     async def __aexit__(self, exc_type, exc_val, exc_tb):
#         """Clean up MCP server connection resources."""
#         try:
#             if self._session_ctx:
#                 await self._session_ctx.__aexit__(exc_type, exc_val, exc_tb)
#             if self._rw_ctx:
#                 await self._rw_ctx.__aexit__(exc_type, exc_val, exc_tb)
#         except Exception as e:
#             print(f"Error cleaning up MCP connection: {e}")
#         finally:
#             self.session = None
#             self._session_ctx = None
#             self._rw_ctx = None

#     async def list_tools(self) -> Any:
#         """Retrieve available tools from the MCP server."""
#         response = await self.session.list_tools()
#         return response.tools

#     async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
#         """Call a tool on MCP server with the given arguments."""
#         return await self.session.call_tool(tool_name, arguments)


# class MCPConnectionStdio(MCPConnection):
#     """MCP connection using standard input/output."""

#     def __init__(self, command: str, args: Optional[List[str]] = None, env: Optional[Dict[str, str]] = None):
#         super().__init__()
#         self.command = command
#         self.args = args
#         self.env = env

#     async def _create_rw_context(self):
#         return stdio_client(StdioServerParameters(command=self.command, args=self.args, env=self.env))


# class MCPConnectionSSE(MCPConnection):
#     """MCP connection using Server-Sent Events."""

#     def __init__(self, url: str, headers: Optional[Dict[str, str]] = None):
#         super().__init__()
#         self.url = url
#         self.headers = headers

#     async def _create_rw_context(self):
#         return sse_client(url=self.url, headers=self.headers)
