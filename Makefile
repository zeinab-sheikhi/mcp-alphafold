.PHONY: help run-server clean install install-uv build-docker run-docker checks update-pre-commit type

UV_COMMAND := uv

help:
	@echo "Available commands:"
	@echo "  make server  - Run the MCP server"
	@echo "  make clean   - Clean up cache files"

run-server:
	uv run python src/mcp_alphafold/mcp_server.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".uv" -exec rm -rf {} +
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	rm -rf .cache
	rm -rf .env
	rm -rf .env.local
	rm -rf .env.development.local
	rm -rf .env.test.local

install-uv:
	@which $(UV_COMMAND) >/dev/null 2>&1 || (echo "Could not find 'uv'! Installing..."; curl -LsSf https://astral.sh/uv/install.sh | sh)

install: install-uv
	uv sync --all-extras

build-docker:
	docker build -t mcp-alphafold .

run-docker:
	docker run -p 8050:8050 mcp-alphafold

checks:
	uv run pre-commit run --all-files

update-pre-commit:
	uv run pre-commit autoupdate

lint:
	uv run ruff check --fix src tests
	uv run ruff format --check src tests

type:
	uv run mypy src --install-types --non-interactive --show-traceback

test:
	uv run pytest tests/

test-coverage:
	uv run pytest --cov=mcp_alphafold --cov-report=term-missing
