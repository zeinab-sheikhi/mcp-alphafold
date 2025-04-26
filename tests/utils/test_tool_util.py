from pathlib import Path

import pytest

from mcp_alphafold.server.tools.utils import load_docstring, with_docstring


@pytest.fixture
def mock_docs_dir(tmp_path, monkeypatch):
    """Create a mock docs directory with test files."""
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()

    test_md = docs_dir.joinpath("test.md")
    test_md.write_text("This is a test documentation")

    def mock_parent_dir(*args, **kwargs):
        return tmp_path

    monkeypatch.setattr(Path, "parent", property(mock_parent_dir))
    return docs_dir


def test_load_docstring_existing_file(mock_docs_dir):
    """Test laoding docstring from an existing file."""
    content = load_docstring("test.md")
    assert content == "This is a test documentation"


def test_load_docstring_missing_file(mock_docs_dir):
    """Test loading docstring from a non-existent file."""
    content = load_docstring("nonexistent.md")
    assert content == "Documentation file nonexistent.md not found."


def test_with_docstring_decorator(mock_docs_dir):
    """Test the with_docstring decorator."""

    @with_docstring("test.md")
    def test_function():
        pass

    assert test_function.__doc__ == "This is a test documentation"
