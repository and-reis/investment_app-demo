import os
import requests
from app.models import User
from app.dbconfig import Database

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

def gen_portfolio_add_balance_with_endpoint(user: dict):

    amount_balance = 40     
    response = requests.post(f"{BASE_URL}/wallet/add_balance?amount={amount_balance}&token={user['token']}")

    if response.status_code == 200:
        print(f"Balance + : {amount_balance} updated successfull.")
    else:
        raise RuntimeError(f"Error on update balance: {response.status_code}, {response.text}")


def gen_portfolio_buy_trade_with_endpoint(user: dict):

    trade_data = {
        "asset_symbol": "BTC",
        "trade_type": "buy",
        "amount_val": 50
        }    
    response = requests.post(f"{BASE_URL}/portfolio/buy?token={user['token']}", json=trade_data)

    if response.status_code == 200:
        print(f"Trade type: {trade_data['trade_type']} generated successfull.")
    else:
        raise RuntimeError(f"Error on create trade: {response.status_code}, {response.text}")
    
def gen_portfolio_sell_trade_with_endpoint(user: dict):

    trade_data = {
        "asset_symbol": "BTC",
        "trade_type": "sell",
        "perc_withdraw": 100,
        "qty": 0
        }    
    response = requests.post(f"{BASE_URL}/portfolio/sell?token={user['token']}", json=trade_data)

    if response.status_code == 200:
        print(f"Trade type: {trade_data['trade_type']} generated successfull.")
    else:
        raise RuntimeError(f"Error on create trade: {response.status_code}, {response.text}")
    
db = Database()
session = db.get_session()
email = 'client-01@example.com'

user_registered = session.query(User.user_id, User.username, User.token).filter(User.email == email).first()._mapping

gen_portfolio_add_balance_with_endpoint(user_registered)

gen_portfolio_buy_trade_with_endpoint(user_registered)

gen_portfolio_sell_trade_with_endpoint(user_registered)


    


