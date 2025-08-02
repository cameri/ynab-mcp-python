# Gemini Project Guide

This document provides guidance for Gemini on how to interact with and manage the `ynab-mcp-python` project.

## Project Overview

This project is a Python application for the YNAB Multi-Currency Processor (MCP) server. It uses `poetry` for dependency
management and `ruff` for linting.

## Documentation (`docs/` folder)

The `docs/` folder contains important project documentation:

- `docs/product.md`: Describes the product vision, features, and overall goals.
- `docs/requirements.md`: Details the functional and non-functional requirements of the application.
- `docs/structure.md`: Outlines the project's directory structure and key components.
- `docs/specs/`: Contains detailed specifications for various parts of the project.

### Keeping Documentation Up-to-Date

- **`docs/product.md`**: Should be updated when there are changes to the product's vision, major features, or strategic
  direction.
- **`docs/requirements.md`**: Should be updated whenever new requirements are identified, existing ones are modified, or
  requirements are implemented/removed.
- **`docs/structure.md`**: Should be updated whenever the project's directory structure changes significantly (e.g., new
  top-level directories, major refactoring of existing ones).

### Creating a New Specification

To create a new specification document within `docs/specs/`, follow these steps:

1. **Copy the template:** Copy the contents of `docs/specs/template/` to a new directory within `docs/specs/` that
   reflects the name of your new spec (e.g., `docs/specs/new_feature_name/`).

   ```bash
   cp -r docs/specs/template docs/specs/your_new_spec_name
   ```

1. **Rename and edit files:** Rename `design.md`, `requirements.md`, and `tasks.md` within your new spec directory as
   appropriate, and fill them with the relevant content for your specification.

1. **Update `docs/specs/README.md`:** Add a link to your new specification in `docs/specs/README.md` to ensure it's
   discoverable.

## Spec-Driven Development and EARS Pattern

All new features and significant changes in this project will adhere to a Spec-Driven Development approach, utilizing
the Easy Approach to Requirements Syntax (EARS) pattern for defining requirements.

- **Spec-Driven Development**: This methodology emphasizes writing detailed specifications before implementation. It
  ensures a clear understanding of requirements, design, and expected behavior, leading to more robust and maintainable
  code.
- **EARS Pattern**: Requirements will be formulated using the EARS pattern (e.g., "WHEN <trigger> IF <precondition> THEN
  <system response> FOR <feature>"). This structured approach enhances clarity, reduces ambiguity, and facilitates
  automated testing.

By adopting these practices, we aim to improve the quality, consistency, and predictability of our development process.

## Development Workflow

### Running Linting

To run the linter (Ruff) and `mdformat` for markdown files:

```bash
poetry run ruff check .
poetry run mdformat --check .
```

To automatically fix linting issues:

```bash
poetry run ruff check . --fix
poetry run mdformat .
```

### Building the Application

This project is primarily a Python application. Building typically involves installing dependencies:

```bash
poetry install
```

### Running the Application

To run the main application (the YNAB MCP server):

```bash
poetry run python src/ynab_mcp_server/main.py
```

### Running Tests

To run the project's tests:

```bash
poetry run pytest
```
