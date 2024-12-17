# -*- coding: utf-8 -*-
"""
Created on Fri Dec 6 09:20:30 2024

@author: Derson

This is an example script for retrieving the PnL (Profit and Loss) through the endpoint.
"""
import os
from app.dbconfig import Database
from app.services.user import UserService
from app.services.portfolio import PortfolioService
import requests

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
endpoint = "/portfolio/pnl"

user_data = {
    "username": "Client 01",
    "email": "client-02@example.com",
    "token": "client01"
}

# Query the user to check if they exist and retrieve the token
db = Database()
session = db.get_session()
user = UserService.get_user_by_email(user_data['email'], session)

# Retrieve the PnL for the user's portfolio
pnl = PortfolioService.get_pnl(user.user_id, session)
print(pnl)

# Fetch PnL via the API endpoint
response = requests.get(BASE_URL + endpoint + f"?token={user.token}")
print(response.json())
