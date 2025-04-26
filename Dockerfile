FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml uv.lock README.md ./
COPY src/ ./src

# install uv
RUN pip install --no-cache-dir uv

ENV PATH="/root/.local/bin:/app/.venv/bin:$PATH"

# install dependecies
RUN uv sync && \
    uv pip install -e . && \
    uv cache clean

# Expose the port the server runs on
EXPOSE 8050

CMD ["mcp-server-alphafold"]
