# Design for Lookup All Budgets

## Tool Implementation

This specification outlines the design for a tool within the YNAB MCP server that, when invoked, will trigger the lookup
of all YNAB budgets.

## Interaction with YNAB API

- The tool will make a direct HTTPS request to the YNAB API to retrieve the list of budgets.
- The endpoint to be used is `https://api.ynab.com/v1/budgets`.
- The request will be a GET request.
- The request must be authenticated by including the user's YNAB API token in the `Authorization` header as a Bearer token.
- The tool will parse the JSON response from the API and return the list of budgets.
