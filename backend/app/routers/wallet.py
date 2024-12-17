# -*- coding: utf-8 -*-
"""
Wallet management endpoints.

This module provides endpoints for managing user wallets, including adding balance
and retrieving the current wallet balance.

Created on Sat Nov 30 13:29:04 2024

@author: Derson
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db_session
from app.services.wallet import WalletService
from app.dependencies import get_current_user
from decimal import Decimal

router = APIRouter()

@router.post("/add_balance", summary="Add balance to the wallet")
def add_balance(
    amount: float,
    session: Session = Depends(get_db_session),
    user=Depends(get_current_user),
):
    """
    Adds balance to the user's wallet.

    Parameters
    ----------
    amount : float
        The amount to add to the wallet. Must be greater than zero.
    session : sqlalchemy.orm.Session
        The database session.
    user : dict
        The current authenticated user, provided by `get_current_user`.

    Returns
    -------
    dict
        A message confirming the operation and the new wallet balance.

    Raises
    ------
    HTTPException
        If the amount is invalid or an error occurs during the operation.
    """
    if amount <= 0:
        raise HTTPException(status_code=400, detail="The amount must be greater than zero.")
    try:
        new_balance = WalletService.update_balance(user["user_id"], Decimal(amount), session)
        return {"message": "Balance added successfully.", "new_balance": new_balance}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding balance: {str(e)}")


@router.get("/get_balance", summary="Retrieve wallet balance")
def get_wallet_balance(
    session: Session = Depends(get_db_session),
    user=Depends(get_current_user),
):
    """
    Retrieves the current wallet balance for the authenticated user.

    Parameters
    ----------
    session : sqlalchemy.orm.Session
        The database session.
    user : dict
        The current authenticated user, provided by `get_current_user`.

    Returns
    -------
    dict
        The current wallet balance.
    """
    balance = WalletService.get_balance(user["user_id"], session)
    return {"balance": balance}
