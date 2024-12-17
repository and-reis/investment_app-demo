# -*- coding: utf-8 -*-
"""
Created on Tue Dec 04 15:13:06 2024

@author: Derson

This script demonstrates retrieving the latest price for a given asset symbol (e.g., BTC) using a price service.
It includes error handling for cases where the price retrieval fails.
"""
from datetime import datetime as dt, timedelta, timezone
from app.services.prices import PriceService
from app.dbconfig import Database

# Initialize database and session
db = Database()
session = db.get_session()

# Define the asset symbol to retrieve
symbol = 'BTC'
full_symbol = f"{symbol.upper()}{PriceService.SYMBOL_PAIR}"
price_service = PriceService()

"""
try:
    # Retrieve the latest price for the asset
    price = price_service.get_price(asset_symbol=symbol, from_api=True)
    print(f"Price for {symbol}: {price}")
except Exception as e:
    # Handle errors during price retrieval
    print(f"Error retrieving price for {symbol}: {e}")
"""

# Example for historical data (uncomment to use)
v_date = dt.now(timezone.utc) - timedelta(days=3)
prices = price_service.get_ohlc(full_symbol, '1d', since=v_date)
print(prices)