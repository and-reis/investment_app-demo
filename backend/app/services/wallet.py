# -*- coding: utf-8 -*-
"""
Service layer for Wallet operations.

This module provides business logic for managing user wallets, including 
retrieving and updating wallet balances.

Created on Fri Nov 29 08:51:13 2024

@author: Derson
"""

from sqlalchemy.orm import Session
from app.models import Wallet
from decimal import Decimal


class WalletService:
    """
    Service class for managing wallet-related operations.
    """

    @staticmethod
    def get_balance(user_id: int, session: Session) -> Decimal:
        """
        Retrieves the current balance of the user's wallet.

        Parameters
        ----------
        user_id : int
            The ID of the user whose wallet balance is being retrieved.
        session : sqlalchemy.orm.Session
            The database session.

        Returns
        -------
        Decimal
            The current wallet balance. Returns 0.0 if the wallet does not exist.
        """
        wallet = session.query(Wallet).filter_by(user_id=user_id).first()
        if not wallet:
            return Decimal('0.0')
        return wallet.balance

    @staticmethod
    def update_balance(user_id: int, amount: Decimal, session: Session) -> Decimal:
        """
        Updates the balance of the user's wallet.

        Parameters
        ----------
        user_id : int
            The ID of the user whose wallet balance is being updated.
        amount : Decimal
            The amount to add to the wallet balance. Can be negative for deductions.
        session : sqlalchemy.orm.Session
            The database session.

        Returns
        -------
        Decimal
            The updated wallet balance.

        Raises
        ------
        ValueError
            If the updated balance becomes negative.
        """
        wallet = session.query(Wallet).filter_by(user_id=user_id).first()
        if not wallet:
            wallet = Wallet(user_id=user_id, balance=Decimal('0.0'))
        
        wallet.balance += amount
        if wallet.balance < 0:
            raise ValueError("Insufficient wallet balance.")
        session.commit()
        session.refresh(wallet)
        return wallet.balance