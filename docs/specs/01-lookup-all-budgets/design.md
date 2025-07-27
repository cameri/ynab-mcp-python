# Design for Lookup All Budgets

## Tool Implementation

This specification outlines the design for a tool within the YNAB MCP server that, when invoked, will trigger the lookup of all YNAB budgets.

## Interaction with YNAB SDK

- The `ynab-sdk-python` library will be used to interact with the YNAB API.
- An instance of `ynab.api.client.Client` will be initialized with the user's YNAB API token.
- The `client.budgets.get_budgets()` method will be called to retrieve the list of budgets.
- The tool will return the list of budgets.
