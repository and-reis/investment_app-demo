# -*- coding: utf-8 -*-
"""
Created on Fri Dec 6 09:20:30 2024

@author: Derson

This is an example script for querying the user's wallet balance through the endpoint.
"""
import os
from app.dbconfig import Database
from app.services.user import UserService
import requests

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
endpoint = "/wallet/get_balance"

user_data = {
    "username": "Client 01",
    "email": "client-01@example.com",
    "token": "client01"
}

# Query the user to check if they exist and retrieve the token
db = Database()
session = db.get_session()
user = UserService.get_user_by_email(user_data['email'], session)

# Make a request to the endpoint to fetch the wallet balance
response = requests.get(BASE_URL + endpoint + f"?token={user.token}")

# Print the response JSON containing the balance
print(response.json())