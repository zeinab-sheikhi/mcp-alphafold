"""Tool documentation loader with format support."""

import functools
from pathlib import Path
from typing import Any, Dict, Optional


class DocLoader:
    def __init__(self):
        self._docs_dir = Path(__file__).parent.parent / "docs"
        self._cache: Dict[str, Any] = {}

    def get_doc(self, tool_name: str) -> Optional[str]:
        """Get documentation for a tool with caching."""

        if tool_name in self._cache:
            return self._cache[tool_name]

        doc_path = self._docs_dir / f"{tool_name}"
        try:
            content = doc_path.read_text()
            self._cache[tool_name] = content
            return content
        except FileNotFoundError as err:
            raise FileNotFoundError(f"Documentation file {doc_path} not found.") from err

    def with_docstring(self, tool_name: str):
        """Decorator to add documentation to a function."""

        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            doc = self.get_doc(tool_name)
            wrapper.__doc__ = doc
            return wrapper

        return decorator
