import asyncio
import signal
from contextlib import asynccontextmanager
from typing import Any, Dict, List, Literal, Optional, Union

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.utilities.logging import get_logger

from mcp_alphafold.server.tools.alphafold import (
    get_alpha_fold_prediction,
    get_annotations,
    get_uniprot_summary,
)
from mcp_alphafold.server.tools.utils import with_docstring
from mcp_alphafold.settings import settings

httpx_logger = get_logger("httpx")
httpx_logger.setLevel("WARN")

logger = get_logger(__name__)
logger.setLevel("INFO")


class AlphFoldMCPServer:
    def __init__(self):
        self.app = FastMCP(
            name=settings.SERVER_NAME,
            host=settings.SERVER_HOST,
            port=settings.SERVER_PORT,
        )
        self._setup_signal_handlers()
        self._setup_tools()
        self.should_exit = False

    def _setup_signal_handlers(self):
        """Setup handlers for graceful shutdown."""
        signals = (signal.SIGTERM, signal.SIGINT)
        for sig in signals:
            signal.signal(sig, self._handle_exit)

    def _handle_exit(self, signum, frame):
        """Handle shutdown signal."""
        if self.should_exit:
            logger.warning("Forced exit requested")
            raise SystemExit(1)

        logger.info("Shutting down initialized...")
        self.should_exit = True
        asyncio.create_task(self._shutdown())

    async def _shutdown(self):
        """Perform shutdown task."""
        logger.info("Shutting down server...")

        # close any open connections
        await self._cleanup_connections()

        if hasattr(self.app, "server"):
            self.app.server.should_exit = True
            await self.app.server.shutdown()

        logger.info("Server shutdown complete")
        raise SystemExit(0)

    async def _cleanup_connections(self):
        """Cleanup any open connections."""
        from mcp_alphafold.utils.http_util import get_cache

        try:
            cache = get_cache()
            cache.close()
            logger.info("Cache connections closed")
        except Exception as e:
            logger.error(f"Error closing cache: {e}")

    def _setup_tools(self):
        """Setup MCP tools."""

        @with_docstring("alphafold_prediction.md")
        @self.app.tool()
        async def alpha_fold_prediction_tool(
            qualifier: str,
            sequence_checksum: Optional[str] = None,
        ) -> Union[str, Dict[str, Any], List[Any]]:
            return await get_alpha_fold_prediction(qualifier, sequence_checksum)

        @with_docstring("uniprot_summary.md")
        @self.app.tool()
        async def uniprot_summary_tool(qualifier: str) -> Union[str, Dict[str, Any]]:
            return await get_uniprot_summary(qualifier)

        @with_docstring("uniprot_annotations.md")
        @self.app.tool()
        async def annotations_tool(
            qualifier: str,
            annotation_type: str = "MUTAGEN",
        ) -> Union[str, Dict[str, Any]]:
            return await get_annotations(qualifier, annotation_type)

    @asynccontextmanager
    async def lifespan(self):
        """Server lifespan context manager."""
        logger.info(f"Starting {settings.SERVER_NAME} server... on {settings.SERVER_HOST}:{settings.SERVER_PORT}")
        try:
            yield
        finally:
            await self._cleanup_connections()
            logger.info("Server stopped")

    def run(self, transport: Literal["stdio", "sse"] = "sse"):
        """Run the server with specified transport mode."""
        try:

            async def _run():
                async with self.lifespan():
                    await self.app.run(transport=transport)

            if transport == "sse":
                # For SSE mode, use asyncio.run
                asyncio.run(_run())
            else:
                # For STDIO mode, use the event loop directly
                loop = asyncio.get_event_loop()
                loop.run_until_complete(_run())

        except KeyboardInterrupt:
            logger.info("Server shutdown requested")
        except Exception as e:
            logger.error(f"Server error: {e}")
            raise
        finally:
            logger.info("Server stopped")


server = AlphFoldMCPServer()
