import pytest
from unittest.mock import MagicMock, patch
from src.ynab_mcp_server.main import YnabMcpServer
from ynab_sdk.api.models.budget_detail import BudgetDetail
from ynab_sdk.api.models.budget_detail_response import BudgetDetailResponse


@pytest.fixture
def mcp_server():
    return YnabMcpServer()


@patch("src.ynab_mcp_server.main.Client")
def test_get_budgets_tool_success(mock_client_class, mcp_server):
    mock_client_instance = MagicMock()
    mock_client_class.return_value = mock_client_instance

    # Mock the response from client.budgets.get_budgets()
    mock_budget = BudgetDetail(
        id="123",
        name="Test Budget",
        last_modified_on="2024-01-01T00:00:00Z",
        first_month="2024-01-01",
        last_month="2024-12-31",
        date_format=None,
        currency_format=None,
        accounts=[],
        payees=[],
        payee_locations=[],
        category_groups=[],
        categories=[],
        months=[],
        transactions=[],
        subtransactions=[],
        scheduled_transactions=[],
        scheduled_subtransactions=[],
    )
    mock_budgets_response = BudgetDetailResponse(data=MagicMock(budgets=[mock_budget]))
    mock_client_instance.budgets.get_budgets.return_value = mock_budgets_response

    api_token = "TEST_API_TOKEN"
    result = mcp_server.get_budgets(api_token)

    mock_client_class.assert_called_once_with(api_token)
    mock_client_instance.budgets.get_budgets.assert_called_once()
    assert len(result) == 1
    assert result[0]["id"] == "123"
    assert result[0]["name"] == "Test Budget"


@patch("src.ynab_mcp_server.main.Client")
def test_get_budgets_tool_failure(mock_client_class, mcp_server):
    mock_client_instance = MagicMock()
    mock_client_class.return_value = mock_client_instance

    mock_client_instance.budgets.get_budgets.side_effect = Exception("Unauthorized")

    api_token = "INVALID_TOKEN"
    with pytest.raises(Exception, match="Failed to retrieve budgets: Unauthorized"):
        mcp_server.get_budgets(api_token)

    mock_client_class.assert_called_once_with(api_token)
    mock_client_instance.budgets.get_budgets.assert_called_once()
