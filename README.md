# YNAB MCP Server

[![CI/CD](https://github.com/cameri/ynab-mcp-python/actions/workflows/main.yml/badge.svg)](https://github.com/cameri/ynab-mcp-python/actions/workflows/main.yml)
[![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![License](https://img.shields.io/github/license/cameri/ynab-mcp-python)](https://github.com/cameri/ynab-mcp-python/blob/main/LICENSE)

A Python-based MCP (Machine-readable Co-operation Plan) Server for interfacing with the YNAB (You Need A Budget) API.

## About The Project

This project provides a server that acts as a bridge between a client application and the YNAB API. It is designed to
work with both stdio and HTTP transports, making it flexible for various client implementations. The core idea is to
provide use-case-driven tools rather than a direct 1-to-1 mapping of YNAB API endpoints.

We follow a spec-driven development approach. You can find our documentation in the `docs/` directory.

## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

- [Python 3.12+](https://www.python.org/)
- [Poetry](https://python-poetry.org/)
- [pyenv](https://github.com/pyenv/pyenv) (recommended for managing Python versions)

### Installation

1. **Clone the repo**

   ```sh
   git clone https://github.com/cameri/ynab-mcp-python.git
   cd ynab-mcp-python
   ```

1. **Set up the Python version**

   ```sh
   pyenv install 3.12
   pyenv local 3.12
   ```

1. **Install dependencies**

   ```sh
   poetry install
   ```

1. **Install pre-commit hooks**

   ```sh
   poetry run pre-commit install
   ```

## Usage

The server can be started with either `stdio` or `http` transport.

```sh
poetry run python src/ynab_mcp_server/main.py --transport stdio
```

or

```sh
poetry run python src/ynab_mcp_server/main.py --transport http
```

*(Note: The implementation of the server is not yet complete.)*

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any
contributions you make are **greatly appreciated**.

Please read our [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting
pull requests to us.

## License

Distributed under the MIT License. See `LICENSE` for more information.
