"""
Functional tests for portfolio-related endpoints.

This module contains tests to validate the behavior of portfolio management
endpoints, including adding balance, buying assets, and selling assets.

Created on Thu Dec 5 21:05:42 2024

@author: Derson
"""

import requests

BASE_URL = "http://localhost:8000"  # Adjust as needed


def test_add_balance(existing_user):
    """
    Tests the `/wallet/add_balance` endpoint to add balance to a user's wallet.

    Parameters
    ----------
    existing_user : dict
        A fixture representing an existing user with a valid token.

    Assertions
    ----------
    - Ensures the request returns a 200 status code.
    - Validates that the balance addition operation is successful.

    Notes
    -----
    The `amount` query parameter specifies the amount to be added.
    """
    user = existing_user
    amount_balance = 40

    response = requests.post(
        f"{BASE_URL}/wallet/add_balance?amount={amount_balance}&token={user['token']}"
    )
    assert response.status_code == 200, f"Error on adding balance: {response.text}"


def test_buy_trade(existing_user):
    """
    Tests the `/portfolio/buy` endpoint to create a buy transaction.

    Parameters
    ----------
    existing_user : dict
        A fixture representing an existing user with a valid token.

    Assertions
    ----------
    - Ensures the request returns a 200 status code.
    - Validates that the buy trade operation is successful.

    Notes
    -----
    The request body contains the trade details such as `asset_symbol`, `trade_type`, and `amount_val`.
    """
    user = existing_user
    trade_data = {
        "asset_symbol": "BTC",
        "trade_type": "buy",
        "amount_val": 50,
    }

    response = requests.post(
        f"{BASE_URL}/portfolio/buy?token={user['token']}", json=trade_data
    )

    assert response.status_code == 200, f"Error on create buy trade: {response.text}"


def test_sell_trade(existing_user):
    """
    Tests the `/portfolio/sell` endpoint to create a sell transaction.

    Parameters
    ----------
    existing_user : dict
        A fixture representing an existing user with a valid token.

    Assertions
    ----------
    - Ensures the request returns a 200 status code.
    - Validates that the sell trade operation is successful.

    Notes
    -----
    The request body contains the trade details such as `asset_symbol`, `trade_type`, `perc_withdraw`, and `qty`.
    """
    user = existing_user
    trade_data = {
        "asset_symbol": "BTC",
        "trade_type": "sell",
        "perc_withdraw": 100,
        "qty": 0,
    }

    response = requests.post(
        f"{BASE_URL}/portfolio/sell?token={user['token']}", json=trade_data
    )

    assert response.status_code == 200, f"Error on create sale trade: {response.text}"
