"""Tools that interface with MCP servers."""

from .base import BaseTool
from typing import Any, Dict


class MCPTool(BaseTool):
    def __init__(
        self,
        name: str, 
        description: str, 
        input_schema: Dict[str, Any],
        connection: MCPConnection,
    ):
        super().__init__(
            name=name, description=description, input_schema=input_schema,
        )
        self.connection = connection

    async def execute(self, **kwargs) -> str:
        """Execute the MCP tool with the given input_schema."""
        try:
            result = await self.connection.call_tool(
                self.name, arguments=kwargs
            )
            if hasattr(result, "content") and result.content:
                for item in result.content:
                    if getattr(item, "type", None) == "text":
                        return item.text
            return "No text content in tool response"
        except Exception as e:
            return f"Error executing {self.name}: {e}"
