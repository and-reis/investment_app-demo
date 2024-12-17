# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 09:23:01 2024

@author: Derson

This is an example script for creating a user directly in the database using ORM.
"""

from app.dbconfig import Database
from app.schemas.user import UserCreate
from app.services.user import UserService

db = Database()
session = db.get_session()

# Define parameters for the Manager user
manager_data = {
    "username": "Manager 02",
    "email": "manager-02@example.com",
    "password": "test",
    "role": "manager",
    "manager_id": 0
}
# user_data = UserCreate(**manager_data)

# Define parameters for the Client user
client_data = {
    "username": "Client 03",
    "email": "client-03@example.com",
    "password": "test",
    "role": "client",
    "manager_id": 1               
}
# Convert the dictionary parameters to a Pydantic model
user_data = UserCreate(**client_data)

# Create the user in the database using the ORM
user = UserService.create_user(user_data, session)