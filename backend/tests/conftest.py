# -*- coding: utf-8 -*-
"""
Pytest fixtures for testing the Investment App.

This module provides reusable fixtures for setting up the database, creating test
sessions, and ensuring consistent test data.

Created on Thu Dec 5 14:16:17 2024

@author: Derson
"""

import pytest
import os
from sqlalchemy.orm import Session
from app.dbconfig import Database
from app.models import *
from app.schemas.user import UserCreate
from app.services.user import UserService


@pytest.fixture(scope="session")
def test_db():
    """
    Configures the database for testing.

    This fixture sets the `EXECUTION_MODE` to `test` and initializes the database
    connection.

    Returns
    -------
    Database
        An instance of the `Database` configured for testing.
    """
    os.environ["EXECUTION_MODE"] = "test"
    return Database()


@pytest.fixture(scope="session")
def persistent_session(test_db):
    """
    Creates a persistent database session for tests that require it.

    This fixture initializes a single session that persists for the duration of the test session.
    It is useful for setup tasks like creating test data shared across multiple tests.

    Parameters
    ----------
    test_db : Database
        The database instance configured for testing.

    Yields
    ------
    sqlalchemy.orm.Session
        A persistent session for database operations.
    """
    session = test_db.get_session()
    yield session
    test_db.close_session(session)


@pytest.fixture(scope="function")
def test_session(test_db):
    """
    Creates an isolated database session for each test.

    This fixture wraps each test in a database transaction, rolling back all changes
    after the test completes. It ensures that tests are isolated and do not affect each other.

    Parameters
    ----------
    test_db : Database
        The database instance configured for testing.

    Yields
    ------
    sqlalchemy.orm.Session
        A new session bound to a transaction for the test.
    """
    connection = test_db.engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    transaction.rollback()  # Revert changes made during the test
    connection.close()
    session.close()


@pytest.fixture(scope="function")
def cicd_user(persistent_session):
    """
    Ensures that the 'Teste CICD' user exists in the database.

    This fixture checks for the presence of a specific test user in the database and
    creates it if it does not exist. It can be used to simulate user-based tests.

    Parameters
    ----------
    persistent_session : sqlalchemy.orm.Session
        The persistent session for database operations.

    Returns
    -------
    User
        The user instance from the database.
    """
    user_data = UserCreate(
        username="Teste CICD",
        email="cicd@example.com",
        password="cicd",
        role="client",
        manager_id=0,
    )

    try:
        user = UserService.get_user_by_email(user_data.email, persistent_session)
    except ValueError:
        user = UserService.create_user(user_data, persistent_session)

    return user


@pytest.fixture(scope="function")
def existing_user(persistent_session):
    """
    Retrieves an existing user from the database with a token.

    This fixture queries the database for a specific user by email. If the user is not found,
    the test fails.

    Parameters
    ----------
    persistent_session : sqlalchemy.orm.Session
        The persistent session for database operations.

    Returns
    -------
    dict
        A dictionary containing the user's ID, username, and token.

    Raises
    ------
    pytest.fail
        If the user is not found in the database.
    """
    email = "cicd@example.com"
    user = (
        persistent_session.query(User.user_id, User.username, User.token)
        .filter(User.email == email)
        .first()
    )
    if not user:
        pytest.fail(f"User with email {email} not found in the database.")
    return user._mapping
