# MCP-AlphaFold

A Model Context Protocol (MCP) server that provides programmatic access to AlphaFold predictions and UniProt data.
Built with FastMCP and Python, it offers tools for protein structure predictions, UniProt summaries, and protein annotations.

## Requirements
- Python ≥ 3.11
- uv package manager


### ⚙️ Configure Claude Desktop
- Open Claude Desktop settings
- Navigate to Developer section
- Click "Edit Config" and add:
```json
{
  "mcpServers": {
    "mcp_alphafold": {
      "command": "uv",
      "args": [
        "--directory",
        "path to /mcp-alphafold/src/mcp_alphafold",
        "run",
        "mcp-alphafold",
        "--transport",
        "stdio"
      ]
    }
  }
}
   ```
   - Restart Claude Desktop and start chatting about biomedical topics!

### 🐳 Using with Docker

```
"mcpServers": {
  "mcp_alphafold": {
    "command": "docker",
    "args": [
      "run",
      "--rm",
      "-p", "8050:8050",
      "zeinabsheikhi/mcp-alphafold:0.1.0"
    ]
  }
}
```

### 🔧 Tools

The server offers these core tools:

#### 🧬 AlphaFold Tools
- `alphafold_prediction`
    - Retrieves protein structure predictions using AlphaFold. Input a protein identifier or sequence checksum to get structural predictions.

- `uniprot_summary`
    - Fetches comprehensive protein summaries from UniProt database, including protein function, domains, and other key characteristics.

- `annotations`
    - Retrieves specific protein annotations including mutations, modifications, and other experimental data. Default annotation type is "MUTAGEN".


## 🚀 Development

### 📦 Prerequisites

1. Install `uv` (Universal Virtualenv):
```bash
# Using pip
pip install uv

# Using Homebrew on macOS
brew install uv

# Using cargo (Rust package manager)
cargo install uv
```

2. Clone the repository and set up development environment:
```bash
# Clone the repository
git clone https://github.com/zeinab-sheikhi/mcp-alphafold.git
cd mcp-alphafold

# Create and activate virtual environment using uv
uv venv
source .venv/bin/activate  # On Unix/macOS
.venv\Scripts\activate     # On Windows

# Install dependencies including dev dependencies
make install
```

3. Run the server with
```make run-server ```

### 🐳 Docker

Build and run the Docker container:

```bash
# Build the image
make build-docker
# Run the container
make run-docker
```
