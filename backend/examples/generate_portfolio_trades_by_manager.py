# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 10:43:02 2024

@author: Derson

This is an example script for simulating buy/sell trades by manager using Python and database libraries.
Considering an existing manager in the database with at least 01 client, we can run the test validating the trade flow of all its clients

"""
from sqlalchemy.orm import aliased
from app.services.portfolio import PortfolioService
from app.services.wallet import WalletService
from app.dbconfig import Database
from app.models import User


def gen_trade_buysell(client_data, session):
    """ Consolidates operations into a single batch to test the buy/sell flow """
    #Add 50.0 to balance
    WalletService.update_balance(client_data['user_id'], 50, session=session)

    trans_buy_data = {
        "asset_symbol": "SOL",
        "trade_type": "buy",
        "amount_val": 50.0 
        }

    trans_sell_data = {
        "asset_symbol": "SOL",
        "trade_type": "sell",
        "perc_withdraw": 100, # Sell 100% of the quantity
        "qty": 0
        }

    # Execute trade operations
    portfolio_service = PortfolioService()
    portfolio_service.add_transaction(trans_buy_data, session, client_id=client_data['user_id'])
    portfolio_service.add_transaction(trans_sell_data, session, client_id=client_data['user_id'])


# Initialize database and session
db = Database()
session = db.get_session()

# Retrieve clients data
mng_email = "manager-02@example.com"

managers = aliased(User)
query = (
        session.query(
            User.user_id,
            User.username
        )
        .join(managers, managers.user_id == User.manager_id)
        .filter(managers.email == mng_email)
    )

#Executes trades for all clients in the manager's portfolio
clients = [ dict(row._mapping) for row in query.all() ]
for client in clients:
    
    gen_trade_buysell(client_data=client, session=session)
    print(f"Trade generated for {client['username']}")


