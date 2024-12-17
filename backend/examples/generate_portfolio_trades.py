# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 10:43:02 2024

@author: Derson

This is an example script for simulating buy and sell trades using Python and database libraries.
"""
from app.services.user import UserService
from app.services.portfolio import PortfolioService
from app.services.wallet import WalletService
from app.dbconfig import Database

def add_balance(user, session):
    # Add balance to the user's wallet
    wallet_data = {
        "user_id": user.user_id,
        "amount_val": 10
    }
    balance = WalletService.update_balance(wallet_data.get('user_id'), wallet_data.get('amount_val'), session)
    return balance

def buy_asset(user, session):
    # Simulate buying an asset
    portfolio_service = PortfolioService()
    transaction_data = {
        "asset_symbol": "SOL",
        "trade_type": "buy",
        "amount_val": 10.0,
        "user_id": user.user_id
    }
    transaction = portfolio_service.add_transaction(transaction_data, session)
    return transaction

def sell_asset(user, session):
    # Simulate selling an asset
    portfolio_service = PortfolioService()
    transaction_data = {
        "asset_symbol": "SOL",
        "trade_type": "sell",
        # "perc_withdraw": 75, # Sell 75% of the quantity
        "perc_withdraw": 100, # Sell 100% of the quantity
        "qty": 0,
        "user_id": user.user_id
    }
    transaction = portfolio_service.add_transaction(transaction_data, session)
    return transaction

# Initialize database and session
db = Database()
session = db.get_session()

# Retrieve user data
email = "client-01@example.com"
user_data = UserService.get_user_by_email(email=email, session=session)

# Execute trade operations
add_balance(user=user_data, session=session)
buy_asset(user=user_data, session=session)
# sell_asset(user=user_data, session=session)

# sell_asset(session)
