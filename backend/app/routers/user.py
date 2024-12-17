# -*- coding: utf-8 -*-
"""
User management endpoints.

This module provides endpoints for registering and retrieving user details.

Created on Thu Nov 28 15:19:05 2024

@author: Derson
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse
from app.services.user import UserService
from app.dependencies import get_current_user, get_db_session

router = APIRouter()

@router.post("/users/register", response_model=UserResponse, summary="Register a new user")
def register_user(data: UserCreate, session: Session = Depends(get_db_session)):
    """
    Registers a new user (client or administrator).

    Parameters
    ----------
    data : UserCreate
        The user data for registration.
    session : sqlalchemy.orm.Session
        The database session.

    Returns
    -------
    UserResponse
        The details of the newly registered user.

    Raises
    ------
    HTTPException
        If the user registration fails due to validation errors.
    """
    try:
        user = UserService.create_user(data, session)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/get_userdata", response_model=UserResponse, summary="Retrieve user data")
def get_user_data(
    session: Session = Depends(get_db_session),
    current_user=Depends(get_current_user)
):
    """
    Retrieves the details of the current authenticated user.

    Parameters
    ----------
    session : sqlalchemy.orm.Session
        The database session.
    current_user : dict
        The current authenticated user, provided by `get_current_user`.

    Returns
    -------
    UserResponse
        The details of the current user.

    Raises
    ------
    HTTPException
        If the user is not found in the database.
    """
    print(f"Current user ID: {current_user['user_id']}")
    
    userdata = UserService.get_user_by_id(current_user['user_id'], session)
    if not userdata:
        raise HTTPException(status_code=404, detail="User not found")
    
    return userdata