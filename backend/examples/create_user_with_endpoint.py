# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 09:23:01 2024

@author: Derson

This is an example script for creating a user through the endpoint.
"""
import os
import requests

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
user_data = {
        "username": "Client 01",
        "email": "client-01@example.com",
        "password": "test",
        "role": "client",
        "manager_id": 0
        }    

# Create the user if it doesn't exist
response = requests.post(f"{BASE_URL}/user/users/register", json=user_data)
if response.status_code == 200:
    print(f"User {user_data['username']} registered.")
else:
    raise RuntimeError(f"Error creating user: {response.status_code}, {response.text}")
