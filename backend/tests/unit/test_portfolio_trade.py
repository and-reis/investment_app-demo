# -*- coding: utf-8 -*-
"""
Unit tests for portfolio trading operations.

This module contains tests to validate portfolio trading operations,
including adding balance, buying and selling assets, and retrieving
portfolio summaries.

Created on Thu Dec 5 20:25:42 2024

@author: Derson
"""

from app.services.portfolio import PortfolioService
from app.services.wallet import WalletService


def test_add_balance(cicd_user, persistent_session):
    """
    Validates that balance can be added to a user's wallet.

    Parameters
    ----------
    cicd_user : User
        A pre-existing user fixture for testing.
    persistent_session : sqlalchemy.orm.Session
        A database session fixture for persistent testing.

    Assertions
    ----------
    - Ensures that the balance is updated and is at least equal to the added amount.
    """
    wallet_data = {
        "user_id": cicd_user.user_id,
        "amount_val": 90,
    }

    balance = WalletService.update_balance(
        wallet_data.get("user_id"), wallet_data.get("amount_val"), persistent_session
    )
    assert balance >= wallet_data.get("amount_val")


def test_buy_asset(cicd_user, persistent_session):
    """
    Simulates the purchase of an asset and validates the transaction.

    Parameters
    ----------
    cicd_user : User
        A pre-existing user fixture for testing.
    persistent_session : sqlalchemy.orm.Session
        A database session fixture for persistent testing.

    Assertions
    ----------
    - Ensures the transaction has the correct asset symbol.
    - Validates that the quantity of the asset purchased is greater than zero.
    """
    portfolio_service = PortfolioService()
    transaction_data = {
        "asset_symbol": "BTC",
        "trade_type": "buy",
        "amount_val": 100.0,
        "user_id": cicd_user.user_id,
    }

    transaction = portfolio_service.add_transaction(transaction_data, persistent_session)
    assert transaction.asset_symbol == "BTCUSDT"
    assert transaction.qty > 0


def test_sell_asset(cicd_user, persistent_session):
    """
    Simulates the sale of an asset and validates the transaction.

    Parameters
    ----------
    cicd_user : User
        A pre-existing user fixture for testing.
    persistent_session : sqlalchemy.orm.Session
        A database session fixture for persistent testing.

    Assertions
    ----------
    - Ensures the transaction has the correct asset symbol.
    - Validates that the quantity sold is greater than zero.
    """
    portfolio_service = PortfolioService()
    transaction_data = {
        "asset_symbol": "BTC",
        "trade_type": "sell",
        "perc_withdraw": 100,  # Sells 100% of the quantity
        "qty": 0,
        "user_id": cicd_user.user_id,
    }
    transaction = portfolio_service.add_transaction(transaction_data, persistent_session)
    assert transaction.asset_symbol == "BTCUSDT"
    assert abs(transaction.qty) > 0


def test_summary(cicd_user, persistent_session):
    """
    Validates that the portfolio summary is generated correctly.

    Parameters
    ----------
    cicd_user : User
        A pre-existing user fixture for testing.
    persistent_session : sqlalchemy.orm.Session
        A database session fixture for persistent testing.

    Assertions
    ----------
    - Ensures that the portfolio summary contains at least one asset.
    """
    portfolio_service = PortfolioService()
    summary = portfolio_service.get_summary(cicd_user.user_id, persistent_session)
    assert len(summary) > 0
