"""Base tool definitions for the agent framework."""

from pydantic import BaseModel, Field
from typing import Any, Dict


class BaseTool(BaseModel):
    """Base class for all agent tools."""
    name: str = Field(
        ...,
        description="The name of the tool",
    )
    description: str = Field(
        ...,
        description="The description of the tool",
    )
    input_schema: Dict[str, Any] = Field(
        ...,
        description="The input schema defining the tool's parameters",
    )

    def to_dict(self) -> Dict[str, Any]:
        """Convert tool description to Claude format."""
        return {
            "name": self.name, 
            "description": self.description,
            "input_schema": self.input_schema,
        }

    async def execute(self, **kwargs) -> Any:
        """Execture the tool with the given input parameters."""
        raise NotImplementedError(
            "Tool Subclasses must implement execute method."
        )
