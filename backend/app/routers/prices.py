# -*- coding: utf-8 -*-
"""
Price endpoints.

This module provides endpoints for retrieving cryptocurrency prices, 
including fetching current prices from the exchange and the most recent 
prices from the local database.

Created on Tue Nov 26 12:58:45 2024

@author: Derson
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.dependencies import get_database_instance
from app.services.prices import PriceService
from app.schemas.prices import PriceResponse
from app.models import PriceHistory

router = APIRouter()

db = get_database_instance()


@router.get("/current_price/{symbol}", summary="Get current price from the exchange")
def get_current_price(symbol: str):
    """
    Fetches the current price of a cryptocurrency directly from the exchange.

    Parameters
    ----------
    symbol : str
        The symbol of the cryptocurrency (e.g., "BTC").

    Returns
    -------
    dict
        A dictionary containing the symbol and its current price.

    Raises
    ------
    ValueError
        If the price cannot be fetched from the exchange.
    """
    price_service = PriceService()
    try:
        price = price_service.get_price(symbol, session=db.get_session())
        return {"symbol": symbol, "price": price}
    except ValueError:
        return {"error": f"Unable to fetch the price of {symbol}"}


@router.get("/local_price/", response_model=list[PriceResponse], summary="Get recent local prices")
def get_local_price(session: Session = Depends(db.get_session)):
    """
    Fetches the most recent price of assets from the local database.

    Parameters
    ----------
    session : sqlalchemy.orm.Session
        The database session.

    Returns
    -------
    list[PriceResponse]
        A list of the most recent prices for all tracked assets.
    """
    # Subquery to find the latest timestamp for each asset
    latest_timestamp_subquery = (
        session.query(
            PriceHistory.asset_symbol,
            func.max(PriceHistory.timestamp).label("timestamp")
        ).group_by(PriceHistory.asset_symbol)
        .subquery()
    )
    
    # Main query joining price_history with the subquery
    query = (
        session.query(
            PriceHistory.asset_symbol.label('symbol'),
            PriceHistory.open,
            PriceHistory.high,
            PriceHistory.low,
            PriceHistory.close,
            PriceHistory.created_at
        ).join(
            latest_timestamp_subquery,
            (PriceHistory.asset_symbol == latest_timestamp_subquery.c.asset_symbol) &
            (PriceHistory.timestamp == latest_timestamp_subquery.c.timestamp)
        )
    )
    
    return query.all()
