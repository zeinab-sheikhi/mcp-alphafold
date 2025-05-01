import logging
import signal
import sys
from contextlib import contextmanager
from typing import Generator, Literal

from mcp.server.fastmcp import FastMCP

from mcp_alphafold.settings import settings
from mcp_alphafold.tools.alphafold import alphafold_tools

logger = logging.getLogger(__name__)


class AlphaFoldMCP:
    def __init__(
        self,
        name: str = settings.SERVER_NAME,
        host: str = settings.SERVER_HOST,
        port: int = settings.SERVER_PORT,
    ):
        self.app = FastMCP(
            name=name,
            host=host,
            port=port,
        )
        self._register_tools()
        self._shutdown_requested = False

    def _register_tools(self) -> None:
        """Register tools with the MCP server."""
        alphafold_tools(mcp=self.app)

    def _register_prompts(self) -> None:
        """Register prompts with the MCP server."""
        pass

    def _register_resources(self) -> None:
        """Register resources with the MCP server."""
        pass

    def _handle_shutdown(self, signum: int, frame) -> None:
        """Handle shutdown signals gracefully.

        Args:
            signum: Signal number
            frame: Current stack frame
        """
        logger.info("\nShutdown requested. Gracefully stopping the server...")
        self._shutdown_requested = True
        sys.exit(0)

    @contextmanager
    def _setup_signal_handlers(self) -> Generator[None, None, None]:
        """Set up signal handlers for graceful shutdown."""
        # Store previous handlers to restore them later
        previous_sigint = signal.getsignal(signal.SIGINT)
        previous_sigterm = signal.getsignal(signal.SIGTERM)

        # Set up our handlers
        signal.signal(signal.SIGINT, self._handle_shutdown)
        signal.signal(signal.SIGTERM, self._handle_shutdown)

        try:
            yield
        finally:
            # Restore previous signal handlers
            signal.signal(signal.SIGINT, previous_sigint)
            signal.signal(signal.SIGTERM, previous_sigterm)

    def run(self, transport: Literal["stdio", "sse"] = "sse") -> None:
        """Run the AlphaFold MCP server.

        Args:
            transport: Transport to use for MCP communication ("stdio" or "sse")
        """
        with self._setup_signal_handlers():
            try:
                self.app.run(transport=transport)
            except Exception as e:
                sys.exit(1)
