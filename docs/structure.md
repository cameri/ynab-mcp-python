# Project Structure

This document outlines the directory structure of the YNAB MCP Server project.

## Directory Layout

```plain
.
├── docs/                                   # Documentation files
│   └── specs/                              # Specification documents
├── src/                                    # Source code
└── tests/                                  # Test files
```

## Key Directories

- **`docs/`**: Contains project documentation.
- **`src/ynab_mcp_server/`**: The main source code for the MCP server.
- **`tests/`**: Contains tests for the project.

## Environment Management

This project uses `pyenv` to manage Python versions and `poetry` for dependency management. See the `pyproject.toml`
file for a list of dependencies.
