# Builder stage
FROM python:3.12-alpine AS builder

# Install poetry
RUN pip install poetry

# Set poetry to create virtualenv in project
RUN poetry config virtualenvs.in-project true

# Set working directory
WORKDIR /app

# Copy poetry files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry install --no-root --without dev

# Final stage
FROM python:3.12-alpine

# Set working directory
WORKDIR /app

# Copy virtualenv from builder
COPY --from=builder /app/.venv /app/.venv

# Add virtualenv to PATH
ENV PATH="/app/.venv/bin:$PATH"
ENV FASTMCP_EXPERIMENTAL_ENABLE_NEW_OPEN_API_PARSER=true

# Copy application code
COPY src/ /app/src/
COPY open_api_spec.yaml /app/

# Patch fastmcp
COPY fastmcp /app/.venv/lib/python3.12/site-packages/fastmcp

# Run the application
CMD ["fastmcp", "run", "src/ynab_mcp_python/server.py"]