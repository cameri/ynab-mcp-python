import argparse
from modelcontextprotocol import Tool, Server
from ynab_sdk.api.client import Client


class YnabMcpServer:
    def __init__(self):
        self.server = Server()
        self.server.add_tool(self.get_budgets)

    @Tool(
        name="get_budgets",
        description="Retrieves a list of all budgets accessible by the provided YNAB API token.",
        parameters={
            "type": "object",
            "properties": {
                "api_token": {"type": "string", "description": "The YNAB API token."}
            },
            "required": ["api_token"],
        },
        returns={
            "type": "array",
            "items": {
                "type": "object"
            },  # Simplified, ideally would be a more detailed Budget schema
            "description": "A list of YNAB budget objects.",
        },
    )
    async def get_budgets(self, api_token: str):
        try:
            client = Client(api_token)
            budgets_response = client.budgets.get_budgets()
            return [budget.to_dict() for budget in budgets_response.data.budgets]
        except Exception as e:
            # In a real scenario, you'd want more granular error handling
            # and potentially custom exceptions.
            raise Exception(f"Failed to retrieve budgets: {e}")

    def run(self, transport: str):
        if transport == "stdio":
            print("Starting stdio transport...")
            self.server.run_stdio()
        elif transport == "http":
            print("HTTP transport is not yet implemented for MCP tools.")
            # For HTTP, you would typically integrate with a web framework
            # that can expose the MCP server's tools.
            pass


def main():
    parser = argparse.ArgumentParser(description="YNAB MCP Server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "http"],
        required=True,
        help="The transport to use for communication.",
    )
    args = parser.parse_args()

    mcp_server = YnabMcpServer()
    mcp_server.run(args.transport)


if __name__ == "__main__":
    main()
