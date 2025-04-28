# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim AS uv

WORKDIR /app

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=README.md,target=README.md \
    uv sync --locked

COPY pyproject.toml uv.lock README.md ./
COPY src/ /app


# Sync the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install -e .

# Compiling Python source files to bytecode
ENV UV_COMPILE_BYTECODE=1
ENV PATH="/root/.local/bin:/app/.venv/bin:$PATH"

# Expose the port the server runs on
EXPOSE 8000

# CMD ["run-server"]
