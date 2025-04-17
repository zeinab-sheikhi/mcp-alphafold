"""Tool execution utility with parallel execution support."""

import asyncio
from typing import Any, Dict, List
from pathlib import Path


def load_docstring(file_name: str) -> str:
    """Load the docstring from the markdown file."""
    docs_path = Path(__file__).parent.parent / "docs" / file_name
    try:
        with open(docs_path, "r") as file:
            return file.read()
    except FileNotFoundError:
        return f"Documentation file {file_name} not found."


def with_docstring(md_file: str):
    def decorator(func):
        func.__doc__ = load_docstring(md_file)
        return func
    return decorator


async def _execute_single_tool(
        call: Any, tool_dict: Dict[str, Any],
) -> Dict[str, Any]:
    """Execute a single tool and handle the errors."""
    response = {"type": "tool_result", "tool_use_id": call.id}
    try:
        # execute the tool directly
        result = await tool_dict[call.name](**call.input)
        response["content"] = str(result)
    except KeyError:
        response["content"] = f"Tool {call.name} not found."
        response["is_error"] = True

    except Exception as e:
        response["content"] = f"Error executing tool: {str(e)}"
        response["is_error"] = True
    
    return response


async def execute_tools(
        tool_calls: List[Any],
        tool_dict: Dict[str, Any], 
        parallel: bool = True,
) -> List[Dict[str, Any]]:
    """Execute multiple tools sequentially or in parallel."""
    if parallel:
        return await asyncio.gather(
            *[_execute_single_tool(call, tool_dict) for call in tool_calls]
        )
    else:
        return [
            await _execute_single_tool(call, tool_dict) for call in tool_calls
        ]
