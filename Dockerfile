FROM python:3.11-slim 

WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY src/mcp_alphafold/ ./app

# install uv
RUN pip install --no-cache-dir uv

# install dependecies
RUN uv sync 

# Expose the port the server runs on
EXPOSE 8050

CMD ["uv", "run", "app/mcp_server.py"]