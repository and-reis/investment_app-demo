# -*- coding: utf-8 -*-
"""
Unit tests for user creation and management.

This module contains tests to validate user creation, duplication constraints,
and user updates with manager associations.

Created on Thu Dec 5 15:25:46 2024

@author: Derson
"""

import pytest
from app.schemas.user import UserCreate
from app.services.user import UserService


def test_user_duplication(cicd_user, test_session):
    """
    Validates that duplicate users with the same email cannot be created.

    Parameters
    ----------
    cicd_user : User
        A pre-existing user fixture to simulate duplication.
    test_session : sqlalchemy.orm.Session
        A database session fixture for isolated testing.

    Raises
    ------
    ValueError
        If a user with the same email already exists.
    """
    user_data = UserCreate(
        username="Duplicate User",
        email=cicd_user.email,  # Existing email
        password="newpassword",
        role="client",
        manager_id=0,
    )
    with pytest.raises(ValueError):
        UserService.create_user(user_data, test_session)


def test_create_user_with_manager(test_session):
    """
    Validates that a user can be created and associated with an existing manager.

    Parameters
    ----------
    test_session : sqlalchemy.orm.Session
        A database session fixture for isolated testing.

    Assertions
    ----------
    - Ensures the created user is associated with the specified manager.
    - Validates the user's email and role.
    """
    manager_data = UserCreate(
        username="Manager User",
        email="manager@example.com",
        password="password123",
        role="manager",
        manager_id=0,
    )
    manager = UserService.create_user(manager_data, test_session)

    # Create a user associated with the manager
    user_data = UserCreate(
        username="Employee User",
        email="employee@example.com",
        password="password456",
        role="client",
        manager_id=manager.user_id,  # Associate with the created manager
    )
    user = UserService.create_user(user_data, test_session)

    # Assertions
    assert user.manager_id == manager.user_id
    assert user.email == "employee@example.com"
    assert user.role == "client"


def test_update_user_with_manager(test_session, cicd_user):
    """
    Validates that an existing user can be updated to associate with a new manager.

    Parameters
    ----------
    test_session : sqlalchemy.orm.Session
        A database session fixture for isolated testing.
    cicd_user : User
        A pre-existing user fixture to be updated.

    Assertions
    ----------
    - Ensures the user is successfully associated with the new manager.
    - Validates the user's updated role and manager association.
    """
    manager_data = UserCreate(
        username="New Manager",
        email="newmanager@example.com",
        password="password789",
        role="manager",
        manager_id=0,
    )
    manager = UserService.create_user(manager_data, test_session)

    # Update the default user to associate with the manager
    db_user = test_session.merge(cicd_user)  # Ensures the object is attached to the active session
    db_user.manager_id = manager.user_id
    test_session.commit()  # Save the changes in the test session

    # Retrieve the updated user
    updated_user = UserService.get_user_by_email(cicd_user.email, test_session)

    # Assertions
    assert updated_user.manager_id == manager.user_id
    assert updated_user.role == "client"