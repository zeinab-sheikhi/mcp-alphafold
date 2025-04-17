from abc import ABC, abstractmethod
from contextlib import AsyncExitStack
from typing import Any, Dict, List


class BaseMCPClient(ABC):
    """Base class for MCP clients."""
    def __init__(self):
        self.stack = AsyncExitStack()
        self.connection = None
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
            tools = self.connection.list_tools()
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
