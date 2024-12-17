# -*- coding: utf-8 -*-
"""
Schema for Price operations.

This module defines the Pydantic schema used for validation and serialization 
of price-related data in the application.

Created on Thu Nov 28 14:59:59 2024

@author: Derson
"""

from pydantic import BaseModel
from datetime import datetime


class PriceResponse(BaseModel):
    """
    Schema for returning asset price details.

    Attributes
    ----------
    symbol : str
        The unique symbol of the asset (e.g., "BTC").
    open : float
        The opening price of the asset for the given time interval.
    high : float
        The highest price of the asset for the given time interval.
    low : float
        The lowest price of the asset for the given time interval.
    close : float
        The closing price of the asset for the given time interval.
    created_at : datetime
        The timestamp when the price data was recorded.
    """
    symbol: str
    open: float
    high: float
    low: float
    close: float
    created_at: datetime

    model_config = {"from_attributes": True}