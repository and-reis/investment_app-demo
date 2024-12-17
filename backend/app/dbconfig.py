# -*- coding: utf-8 -*-
"""
Database configuration module.

This module provides utilities to manage database connections and sessions 
for the application, including schema selection based on the execution mode.

Created on Tue Nov 26 15:48:32 2024

@author: Derson
"""

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base
from decouple import config

def get_execution_config():
    """
    Retrieves the current execution mode and maps it to the corresponding schema.

    Returns
    -------
    tuple
        A tuple containing:
        - execution_mode (str): The current execution mode ('dev', 'test', 'prod').
        - schema (str): The schema name based on the execution mode.
    """
    execution_mode = config("EXECUTION_MODE", "dev")

    # Define the schema based on the execution mode
    schema_map = {
        "prod": "prod_sc",
        "test": "test_sc",
        "dev" : "dev_sc"
    }
    return execution_mode, schema_map.get(execution_mode, "prod_sc")

class Database:
    """
    Manages database configurations, connections, and sessions.

    Attributes
    ----------
    execution_mode : str
        Current execution mode ('dev', 'test', 'prod').
    schema : str
        Selected schema based on the execution mode.
    DATABASE_URL : str
        Full database connection URL.
    engine : sqlalchemy.engine.base.Engine
        SQLAlchemy engine for database connections.
    SessionLocal : sqlalchemy.orm.session.Session
        SQLAlchemy sessionmaker for managing sessions.

    Methods
    -------
    get_session()
        Creates and returns a new database session.
    close_session(session)
        Closes an existing database session.
    """
    def __init__(self, custom_url=None):
        """
        Initializes the database configuration.

        Parameters
        ----------
        custom_url : str, optional
            Custom database connection URL. If not provided, the configuration 
            is derived from the environment variables.
        """
        self.execution_mode, self.schema = get_execution_config()

        if custom_url:
            self.DATABASE_URL = custom_url
        else:
            # Configure database URL based on the environment
            DB_HOST = (
                "localhost"
                if self.execution_mode == "dev" and config("IS_DOCKER", "true").lower() == "true"
                else config("POSTGRES_HOST")
            )
            DB_PORT = config("POSTGRES_PORT")
            DB_NAME = config("POSTGRES_DB")
            DB_USER = config("POSTGRES_USER")
            DB_PASSWORD = config("POSTGRES_PASSWORD")
            self.DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        
        # Configure the SQLAlchemy engine
        try:
            self.engine = create_engine(
                self.DATABASE_URL,
                connect_args={"options": f"-c search_path={self.schema}"}
            )
        except Exception as e:
            raise ValueError(f"Error creating the engine: {e}")

        # Configure SQLAlchemy session
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_session(self):
        """
        Creates and returns a new database session.

        Returns
        -------
        sqlalchemy.orm.session.Session
            A new database session.
        """
        try:
            session = self.SessionLocal()
            return session
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            return None

    def close_session(self, session):
        """
        Closes an existing database session.

        Parameters
        ----------
        session : sqlalchemy.orm.session.Session
            The database session to close.
        """
        try:
            session.close()
        except Exception as e:
            print(f"Error closing the session: {e}")


# Base for ORM models
_, current_schema = get_execution_config()
Base = declarative_base(metadata=MetaData(schema=current_schema))
