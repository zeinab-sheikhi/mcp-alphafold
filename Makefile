.PHONY: help server clean

help:
	@echo "Available commands:"
	@echo "  make server  - Run the MCP server"
	@echo "  make clean   - Clean up cache files"

server:
	uv run python src/mcp_alphafold/mcp_server.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".uv" -exec rm -rf {} +