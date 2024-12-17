# -*- coding: utf-8 -*-
"""
Unit test for database structure validation.

This module contains a test to ensure that the required tables are created
in the database.

Created on Sun Dec 8 22:32:43 2024

@author: Derson
"""

def test_tables_created(test_session):
    """
    Validates that the necessary tables are created in the local database.

    Parameters
    ----------
    test_session : sqlalchemy.orm.Session
        A database session fixture for isolated testing.

    Assertions
    ----------
    - Ensures that the tables exists in the database.

    Notes
    -----
    The test uses SQLAlchemy's inspector to retrieve the list of table names
    and verifies the presence of specific required tables.
    """
    from sqlalchemy import inspect

    inspector = inspect(test_session.bind)
    tables = inspector.get_table_names()
    print(f"Created tables: {tables}")
    assert "users" in tables
    assert "wallet" in tables
    assert "assets" in tables
    assert "price_history" in tables
    assert "portfolio" in tables
    
    
