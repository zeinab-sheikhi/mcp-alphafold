"""Tool execution utility."""

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
