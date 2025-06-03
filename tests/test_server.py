import signal

import pytest
from fastmcp import FastMCP

from mcp_alphafold.server import AlphaFoldMCP
from mcp_alphafold.settings import settings


def test_init_with_defaults():
    """Test server initialization with default values."""
    server = AlphaFoldMCP()

    assert server.app.name == settings.SERVER_NAME
    assert isinstance(server.app, FastMCP)
    assert server._shutdown_requested is False


def test_register_tools(mocker):
    """Test tools registration."""
    mock_alphafold_tools = mocker.patch("mcp_alphafold.server.alphafold_tools")
    server = AlphaFoldMCP()

    # _register_tools is called in __init__, so the mock should have been called
    mock_alphafold_tools.assert_called_once_with(mcp=server.app)


def test_run_server(mocker):
    """Test server run method."""
    server = AlphaFoldMCP()
    mock_run = mocker.patch.object(server.app, "run")

    # Test with default transport
    server.run(host=settings.SERVER_HOST, port=settings.SERVER_PORT, transport=settings.TRANSPORT)
    mock_run.assert_called_once_with(host=settings.SERVER_HOST, port=settings.SERVER_PORT, transport=settings.TRANSPORT)

    # Test with custom transport
    mock_run.reset_mock()
    server.run(host="localhost", port=8000, transport="stdio")
    mock_run.assert_called_once_with(host="localhost", port=8000, transport="stdio")


def test_signal_handlers(mocker):
    """Test signal handlers setup."""
    mock_signal = mocker.patch("signal.signal")
    server = AlphaFoldMCP()

    with server._setup_signal_handlers():
        # Verify SIGINT handler was set
        mock_signal.assert_any_call(signal.SIGINT, server._handle_shutdown)
        # Verify SIGTERM handler was set
        mock_signal.assert_any_call(signal.SIGTERM, server._handle_shutdown)
        assert mock_signal.call_count == 2


def test_handle_shutdown(mocker):
    """Test shutdown handler."""
    mock_exit = mocker.patch("sys.exit")
    server = AlphaFoldMCP()

    # Simulate shutdown signal
    server._handle_shutdown(None, None)

    assert server._shutdown_requested is True
    mock_exit.assert_called_once_with(0)


def test_run_handles_exceptions(mocker):
    """Test that run method handles exceptions properly."""
    server = AlphaFoldMCP()
    mocker.patch.object(server.app, "run", side_effect=Exception("Test error"))

    with pytest.raises(SystemExit) as exc_info:
        server.run(host=settings.SERVER_HOST, port=settings.SERVER_PORT, transport=settings.TRANSPORT)

    assert exc_info.value.code == 1


def test_signal_handlers_cleanup(mocker):
    """Test that signal handlers are properly restored."""
    mock_signal = mocker.patch("signal.signal")
    original_sigint_handler = signal.getsignal(signal.SIGINT)
    original_sigterm_handler = signal.getsignal(signal.SIGTERM)

    server = AlphaFoldMCP()

    with server._setup_signal_handlers():
        pass

    # Verify handlers were restored
    mock_signal.assert_any_call(signal.SIGINT, original_sigint_handler)
    mock_signal.assert_any_call(signal.SIGTERM, original_sigterm_handler)
