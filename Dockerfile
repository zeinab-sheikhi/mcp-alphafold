FROM python:3.11-slim 

WORKDIR /app

COPY pyproject.toml uv.lock README.md ./
COPY src/mcp_alphafold ./mcp_alphafold

# install uv
RUN pip install --no-cache-dir uv

ENV PATH="/root/.local/bin:$PATH"

# install dependecies
RUN uv sync && \
    uv cache clean

# Expose the port the server runs on
EXPOSE 8050

CMD ["uv", "run", "mcp_alphafold/main.py"]