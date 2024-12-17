# -*- coding: utf-8 -*-
"""
Unit tests for wallet operations.

This module contains tests to validate wallet functionalities, including the creation 
of a user with an initial balance and updating the wallet balance.

Created on Thu Dec 5 20:25:59 2024

@author: Derson
"""

from app.services.wallet import WalletService
from app.services.user import UserService
from app.schemas.user import UserCreate
from decimal import Decimal


def test_create_user_with_initial_balance(test_session):
    """
    Validates the creation of a user and their initial wallet balance.

    Parameters
    ----------
    test_session : sqlalchemy.orm.Session
        A database session fixture for isolated testing.

    Assertions
    ----------
    - Ensures that a newly created user of role `client` is assigned an initial balance of 10.00.
    """
    # Create a client user
    user_data = UserCreate(
        username="Employee User",
        email="employee@example.com",
        password="password456",
        role="client",
        manager_id=0,
    )
    user = UserService.create_user(user_data, test_session)

    # Retrieve the initial wallet balance
    wallet_service = WalletService()
    balance = wallet_service.get_balance(user.user_id, test_session)
    assert balance == Decimal("10.00")


def test_update_balance(test_session):
    """
    Validates the creation of a user and the update of their wallet balance.

    Parameters
    ----------
    test_session : sqlalchemy.orm.Session
        A database session fixture for isolated testing.

    Assertions
    ----------
    - Ensures that a user's wallet balance can be updated correctly.
    - Verifies the final balance after an update operation.
    """
    # Create a client user
    user_data = UserCreate(
        username="Employee User",
        email="employee@example.com",
        password="password456",
        role="client",
        manager_id=0,
    )
    user = UserService.create_user(user_data, test_session)

    # Update the wallet balance
    wallet_service = WalletService()
    wallet_service.update_balance(user.user_id, Decimal("50.00"), test_session)

    # Retrieve the updated balance
    balance = wallet_service.get_balance(user.user_id, test_session)
    assert balance == Decimal("60.00")
