# -*- coding: utf-8 -*-
"""
Access validation and authentication module.

This module provides utilities for user authentication, access validation, and 
database session sharing. It includes token-based authentication and integration 
with FastAPI's dependency injection.

Created on Thu Nov 28 22:33:52 2024

@author: Derson
"""

from fastapi import Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from app.models import User
from app.dbconfig import Database

db_instance = Database()

def get_database_instance():
    """
    Factory function to provide a single database instance.

    Returns
    -------
    Database
        The single database instance used throughout the application.
    """
    return db_instance


def get_db_session():
    """
    Provides a database session.

    Yields
    ------
    sqlalchemy.orm.Session
        A session connected to the database schema in use.
    """
    session = db_instance.get_session()
    print(f"Schema in use: {db_instance.schema}")
    try:
        yield session
    finally:
        session.close()


# Security schema for Swagger
api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

def get_current_user(
    authorization: str = Security(api_key_header),
    token: str = None,
    session: Session = Depends(get_db_session),
):
    """
    Retrieves the currently authenticated user.

    Parameters
    ----------
    authorization : str
        Authorization token provided in the `Authorization` header.
        Supports `Bearer <token>` format or raw token.
    token : str, optional
        Token provided as a query parameter (default is None).
    session : sqlalchemy.orm.Session
        Database session used for validating the token.

    Returns
    -------
    dict
        A dictionary containing user details (`user_id`, `username`, `role`).

    Raises
    ------
    HTTPException
        If the token is missing, invalid, or the user is inactive.
    """
    # Prefer header authorization
    if authorization:
        if authorization.startswith("Bearer "):
            token = authorization.split(" ")[1]  # Extract token after "Bearer"
        else:
            token = authorization  # Assume raw token in header

    # Check if token is provided
    if not token:
        raise HTTPException(
            status_code=400,
            detail="Token not provided. Use 'Authorization: Bearer <token> or pass the token in the URL as ?token=<token>."
        )

    # Clean up token
    token = token.strip()

    # Validate token in database
    user = session.query(User).filter(User.token == token, User.active == True).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token or inactive user.")
    
    return {"user_id": user.user_id, "username": user.username, "role": user.role}
