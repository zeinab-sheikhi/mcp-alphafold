# MCP-AlphaFold

A Model Context Protocol (MCP) server that provides programmatic access to AlphaFold predictions and UniProt data.
Built with FastMCP and Python, it offers tools for protein structure predictions, UniProt summaries, and protein annotations in a containerized environment.

## Requirements
- Python ≥ 3.11
- UV package manager

## Installation

1. Clone the repository:
```bash
git clone https://github.com/zeinab-sheikhi/mcp-alphafold.git
cd mcp-alphafold
```

2. Install dependencies using uv:
```bash
make install
```

### ⚙️ Configuration

Add the server to your `claude_desktop_config.json` with configuration of:

```json
{
  "mcpServers": {
    "mcp_alphafold": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/mcp-alphafold",
        "run",
        "mcp-alphafold"
      ],
    }
  }
}
```
### 🐳 Using with Docker

```json
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

## Available Tools

### 1. AlphaFold Prediction Tool
Retrieves protein structure predictions using AlphaFold. Input a protein identifier or sequence checksum to get structural predictions.

Example usage:
```python
prediction = await alpha_fold_prediction_tool(
    qualifier="P12345",
    sequence_checksum="optional_checksum"
)
```

### 2. UniProt Summary Tool
Fetches comprehensive protein summaries from UniProt database, including protein function, domains, and other key characteristics.

Example usage:
```python
summary = await uniprot_summary_tool(
    qualifier="P12345"
)
```

### 3. Annotations Tool
Retrieves specific protein annotations including mutations, modifications, and other experimental data. Default annotation type is "MUTAGEN".

Example usage:
```python
annotations = await annotations_tool(
    qualifier="P12345",
    annotation_type="MUTAGEN"
)
```
