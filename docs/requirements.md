# Requirements

This document outlines the requirements for the YNAB MCP Server.

## Functional Requirements

The server must be able to:

- Authenticate with the YNAB API using an API key.
- Fetch a list of budgets.
- Fetch a list of accounts for a given budget.
- Fetch a list of categories for a given budget.
- Fetch a list of transactions for a given account.
- Create a new transaction.

## Non-Functional Requirements

- The server should be able to handle concurrent requests.
- The server should log all requests and responses.
- The server should have a comprehensive test suite.

## Out of Scope

- Support for multiple users.
- Real-time data synchronization.

## YNAB Philosophy

It is important to understand the YNAB philosophy when working with this project. Please refer to the following
resources:

- [YNAB's Four Rules](https://www.ynab.com/the-four-rules/)
- [Why YNAB is Different](https://www.ynab.com/why-ynab-is-different/)
