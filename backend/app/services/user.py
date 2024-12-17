# -*- coding: utf-8 -*-
"""
Service layer for User operations.

This module provides business logic for managing users, including creating users, 
retrieving user details, and listing clients managed by a manager.

Created on Thu Nov 28 15:16:38 2024

@author: Derson
"""

import os
import hashlib
from sqlalchemy.orm import Session
from app.models import User, Wallet
from app.schemas.user import UserCreate


class UserService:
    """
    Service class for managing user-related operations.

    Attributes
    ----------
    INITIAL_BALANCE : str
        Default initial balance for new client wallets.
    """
    INITIAL_BALANCE = "10.00"

    @staticmethod
    def create_user(userdata: UserCreate, session: Session) -> User:
        """
        Creates a new user and initializes a wallet for clients.

        Parameters
        ----------
        userdata : UserCreate
            The data for the new user.
        session : sqlalchemy.orm.Session
            The database session.

        Returns
        -------
        User
            The created user object.

        Raises
        ------
        ValueError
            If the email is already registered or the manager is invalid.
        """
        # Check if the email is already registered
        existing_user = session.query(User).filter_by(email=userdata.email).first()
        if existing_user:
            raise ValueError(f"User with email '{userdata.email}' is already registered.")
        
        # Validate manager for clients
        if userdata.role == "client" and userdata.manager_id:
            manager = session.query(User).filter_by(user_id=userdata.manager_id, role="manager").first()
            if not manager:
                raise ValueError(f"Manager with ID {userdata.manager_id} not found or is not a manager.")
        
        # Create the user
        password_hash = hashlib.sha256(userdata.password.encode()).hexdigest()
        salt = os.urandom(16).hex()
        token = hashlib.sha256((userdata.email + salt).encode()).hexdigest()
        user = User(
            username=userdata.username,
            email=userdata.email,
            password_hash=password_hash,
            token=token,
            role=userdata.role,
            manager_id=userdata.manager_id if userdata.role == "client" and userdata.manager_id != 0 else None,
        )
        session.add(user)
        session.commit()
        session.refresh(user)
    
        # Create the client's wallet with an initial balance
        if userdata.role == "client":
            wallet = Wallet(user_id=user.user_id, balance=UserService.INITIAL_BALANCE)
            session.add(wallet)
            session.commit()
    
        return user

    @staticmethod
    def get_user_by_id(user_id: int, session: Session):
        """
        Retrieves a user by their ID.

        Parameters
        ----------
        user_id : int
            The ID of the user to retrieve.
        session : sqlalchemy.orm.Session
            The database session.

        Returns
        -------
        User
            The user object.

        Raises
        ------
        ValueError
            If the user with the given ID is not found.
        """
        user = session.query(User).filter_by(user_id=user_id).first()
        if not user:
            raise ValueError(f"User with ID {user_id} not found.")
        return user

    @staticmethod
    def get_user_by_email(email: str, session: Session):
        """
        Retrieves a user by their email.

        Parameters
        ----------
        email : str
            The email of the user to retrieve.
        session : sqlalchemy.orm.Session
            The database session.

        Returns
        -------
        User
            The user object.

        Raises
        ------
        ValueError
            If the user with the given email is not found.
        """
        user = session.query(User).filter_by(email=email).first()
        if not user:
            raise ValueError(f"User with email: {email} not found.")
        return user

    @staticmethod
    def get_clients_by_manager(manager_id: int, session: Session):
        """
        Retrieves the list of clients managed by a specific manager.

        Parameters
        ----------
        manager_id : int
            The ID of the manager.
        session : sqlalchemy.orm.Session
            The database session.

        Returns
        -------
        list of User
            A list of users who are clients managed by the given manager.
        """
        return session.query(User).filter_by(manager_id=manager_id, role="client").all()
    
    @staticmethod
    def is_client_of_manager(client_id: int, manager_id: int, session: Session) -> bool:
        """
        Verifies if a client belongs to a specific manager.
        
        Parameters
        ----------
        client_id : int
            The ID of the client.
        manager_id : int
            The ID of the manager.        
        session : sqlalchemy.orm.Session
            The database session.
        
        Returns
        -------
        Boolean value
        """
        client = session.query(User).filter_by(user_id=client_id, manager_id=manager_id).first()
        return bool(client)
