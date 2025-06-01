import pytest

from mcp_alphafold.utils.doc import DocLoader


@pytest.fixture
def mock_docs_dir(tmp_path):
    """Create a mock docs directory with test files."""
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()

    test_md = docs_dir.joinpath("test.md")
    test_md.write_text("This is a test documentation")

    return docs_dir


def test_get_doc_existing_file(mock_docs_dir):
    """Test loading docstring from an existing file."""
    loader = DocLoader()
    loader._docs_dir = mock_docs_dir
    content = loader.get_doc("test.md")
    assert content == "This is a test documentation"


def test_get_doc_missing_file(mock_docs_dir):
    """Test loading docstring from a non-existent file."""
    loader = DocLoader()
    loader._docs_dir = mock_docs_dir
    try:
        loader.get_doc("nonexistent.md")
    except FileNotFoundError as e:
        assert "Documentation file" in str(e)
        assert "nonexistent.md" in str(e)
    else:
        raise AssertionError("Expected FileNotFoundError")


def test_with_docstring_decorator(mock_docs_dir):
    """Test the with_docstring decorator."""
    loader = DocLoader()
    loader._docs_dir = mock_docs_dir

    @loader.with_docstring("test.md")
    def test_function():
        pass

    assert test_function.__doc__ == "This is a test documentation"
