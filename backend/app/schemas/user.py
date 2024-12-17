# -*- coding: utf-8 -*-
"""
Schemas for User operations.

This module defines Pydantic schemas used for validation and serialization 
of User-related data in the application.

Created on Thu Nov 28 15:16:26 2024

@author: Derson
"""

from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    """
    Schema for creating a new User.

    Attributes
    ----------
    username : str
        The username of the user.
    email : EmailStr
        The email address of the user.
    password : str
        The password for the user account.
    role : str, optional
        The role of the user (default is "client").
    manager_id : int, optional
        The ID of the manager responsible for the user, if applicable.
    """
    username: str
    email: EmailStr
    password: str
    role: str = "client"  # Default is "client"
    manager_id: Optional[int] = None  # Optional manager association


class UserResponse(BaseModel):
    """
    Schema for returning User details.

    Attributes
    ----------
    user_id : int
        Unique identifier for the user.
    username : str
        The username of the user.
    email : EmailStr
        The email address of the user.
    token : str
        The authentication token for the user.
    manager_id : int, optional
        The ID of the manager responsible for the user, if applicable.
    """
    user_id: int
    username: str
    email: EmailStr
    token: str
    manager_id: Optional[int] = None

    model_config = {"from_attributes": True}


class UserResponseManager(BaseModel):
    """
    Schema for returning limited User details for managers.

    Attributes
    ----------
    user_id : int
        Unique identifier for the user.
    username : str
        The username of the user.
    email : EmailStr
        The email address of the user.
    """
    user_id: int
    username: str
    email: EmailStr

    model_config = {"from_attributes": True}
