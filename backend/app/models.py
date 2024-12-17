# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 12:58:10 2024

@author: Derson
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, TIMESTAMP, ForeignKey, DECIMAL
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.dbconfig import Base

class User(Base):
    """
    Represents a user in the system.
    """
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    # Fields
    user_id = Column(Integer, primary_key=True, index=True, doc="Unique identifier for the user.")
    username = Column(String(50), nullable=False, doc="Username of the user.")
    email = Column(String(100), unique=True, nullable=False, doc="Email address of the user.")
    password_hash = Column(String(200), nullable=False, doc="Hashed password for authentication.")
    token = Column(String(200), unique=True, doc="Static authentication token.")
    active = Column(Boolean, default=True, doc="Indicates if the user account is active.")
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), doc="Timestamp of user account creation.")
    role = Column(String(10), default="client", doc="Role of the user ('client', 'admin', etc.).")
    manager_id = Column(Integer, ForeignKey("users.user_id"), nullable=True, doc="ID of the manager responsible for this user.")


class Wallet(Base):
    """
    Represents a user's wallet for managing their balance.
    """
    __tablename__ = "wallet"
    __table_args__ = {"extend_existing": True}

    # Fields
    wallet_id = Column(Integer, primary_key=True, index=True, doc="Unique identifier for the wallet.")
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, unique=True, doc="ID of the associated user.")
    balance = Column(DECIMAL(18, 8), nullable=False, default=0.0, doc="Balance in the user's wallet.")
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now(), doc="Timestamp of the last wallet update.")
    user = relationship("User")


class Asset(Base):
    """
    Represents a tradable asset.
    """
    __tablename__ = "assets"
    __table_args__ = {"extend_existing": True}

    # Fields
    id = Column(Integer, primary_key=True, index=True, doc="Unique identifier for the asset.")
    name = Column(String(50), nullable=False, doc="Name of the asset (e.g., Bitcoin).")
    symbol = Column(String(10), nullable=False, unique=True, doc="Unique symbol of the asset (e.g., BTC).")
    type = Column(String(20), nullable=False, doc="Type of the asset (e.g., cryptocurrency, stock).")
    active = Column(Boolean, default=True, doc="Indicates if the asset is available for trading.")


class Portfolio(Base):
    """
    Represents a user's portfolio transaction.
    """
    __tablename__ = "portfolio"
    __table_args__ = {"extend_existing": True}

    # Fields
    transaction_id = Column(Integer, primary_key=True, index=True, doc="Unique identifier for the transaction.")
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, doc="ID of the user associated with the transaction.")
    asset_symbol = Column(String(10), nullable=False, doc="Symbol of the traded asset.")
    trade_type = Column(String(10), nullable=False, doc="Type of the trade ('buy' or 'sell').")
    qty = Column(DECIMAL(18, 8), nullable=False, doc="Quantity of the asset traded.")
    net_val = Column(DECIMAL(18, 8), nullable=False, doc="Net value of the transaction after fees.")
    price = Column(DECIMAL(18, 8), nullable=False, default=0.0, doc="Price per unit at the time of the transaction.")
    fee = Column(DECIMAL(18, 8), nullable=False, default=0.0, doc="Fee applied to the transaction.")
    trade_at = Column(TIMESTAMP, server_default=func.now(), doc="Timestamp of the transaction.")
    user = relationship("User")


class PriceHistory(Base):
    """
    Stores the price history of assets.
    """
    __tablename__ = "price_history"
    __table_args__ = {"extend_existing": True}

    # Fields
    id = Column(Integer, primary_key=True, index=True, doc="Unique identifier for the price record.")
    asset_symbol = Column(String(10), nullable=False, doc="Symbol of the asset.")
    timestamp = Column(TIMESTAMP, nullable=False, doc="Timestamp of the price record.")
    interval = Column(String(10), nullable=False, doc="Time interval for the record (e.g., '1m', '1h').")
    open = Column(DECIMAL(18, 8), nullable=False, doc="Open price.")
    high = Column(DECIMAL(18, 8), nullable=False, doc="Highest price.")
    low = Column(DECIMAL(18, 8), nullable=False, doc="Lowest price.")
    close = Column(DECIMAL(18, 8), nullable=False, doc="Closing price.")
    created_at = Column(TIMESTAMP, server_default=func.now(), doc="Timestamp when the record was created.")