import os
from pathlib import Path

import httpx
import yaml
from fastmcp import FastMCP

# Load the OpenAPI spec from YAML file
spec_path = Path(__file__).parent.parent.parent / "open_api_spec.yaml"
with open(spec_path, "r") as f:
    openapi_spec = yaml.safe_load(f)

client = httpx.AsyncClient(
    base_url="https://api.ynab.com/v1",
    headers={"Authorization": f"Bearer {os.getenv('YNAB_API_KEY')}"},
)

mcp = FastMCP.from_openapi(
    openapi_spec=openapi_spec, client=client, name="YNAB MCP Server"
)

if __name__ == "__main__":
    mcp.run(transport="http", port=8000)
