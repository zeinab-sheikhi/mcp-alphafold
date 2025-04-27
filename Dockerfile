# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.13-slim

WORKDIR /app

COPY pyproject.toml uv.lock README.md ./
COPY src/ ./src

ENV PATH="/root/.local/bin:/app/.venv/bin:$PATH"

# install dependecies
RUN uv sync && \
    uv pip install -e . && \
    uv cache clean

# Expose the port the server runs on
EXPOSE 8050

CMD ["mcp-server-alphafold"]
