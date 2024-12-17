# -*- coding: utf-8 -*-
"""
Service layer for Price operations.

This module provides business logic for managing asset prices, including fetching
current prices, historical OHLC data, and saving OHLC data to the database.

Created on Wed Nov 27 15:59:29 2024

@author: Derson
"""

import logging
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from datetime import datetime as dt, timezone, timedelta
from app.models import PriceHistory, Asset
import ccxt

logger = logging.getLogger("app.services.prices")

class PriceService:
    """
    Service class for managing price-related operations.

    Attributes
    ----------
    SYMBOL_PAIR : str
        Default symbol pair for trading pairs (e.g., 'USDT').
    """
    SYMBOL_PAIR = 'USDT'

    def __init__(self):
        """
        Initializes the PriceService with a connection to the Binance API.
        """
        self.exchange = ccxt.binance()

    def get_active_assets(self, session: Session) -> list[Asset]:
        """
        Retrieves a list of active assets.

        Parameters
        ----------
        session : sqlalchemy.orm.Session
            The database session.

        Returns
        -------
        list of Asset
            A list of active assets.
        """
        return session.query(Asset).filter(Asset.active == True).all()

    def get_price(self, asset_symbol: str, session: Session = None, from_api: bool = False) -> float:
        """
        Fetches the current price of an asset.

        Parameters
        ----------
        asset_symbol : str
            The symbol of the asset (e.g., "BTC").
        session : sqlalchemy.orm.Session, optional
            The database session (required if `from_api` is False).
        from_api : bool, optional
            If True, fetches the price directly from the Binance API.

        Returns
        -------
        float
            The current price of the asset.

        Raises
        ------
        ValueError
            If the price cannot be retrieved from the database or API.
        """
        full_symbol = f"{asset_symbol.upper()}{self.SYMBOL_PAIR}"

        if from_api:
            try:
                ticker = self.exchange.fetch_ticker(full_symbol)
                return ticker["last"]
            except Exception as e:
                raise ValueError(f"Error fetching price from API for {full_symbol}: {e}")

        if session is None:
            raise ValueError("A database session is required to fetch prices from history.")

        current_price_record = session.query(PriceHistory.close).filter(
            PriceHistory.asset_symbol == full_symbol,
            PriceHistory.timestamp > dt.now(timezone.utc) - timedelta(hours=1)
        ).order_by(PriceHistory.timestamp.desc()).first()

        if not current_price_record:
            current_price_record = session.query(PriceHistory.close).filter(
                PriceHistory.asset_symbol == full_symbol
            ).order_by(PriceHistory.timestamp.desc()).first()

        if not current_price_record:
            raise ValueError(f"Price not found for {full_symbol} in the database.")

        return current_price_record[0]

    def get_prices(self, symbols: list[str]) -> dict:
        """
        Fetches current prices for multiple cryptocurrencies.

        Parameters
        ----------
        symbols : list of str
            A list of asset symbols to fetch prices for.

        Returns
        -------
        dict
            A dictionary of asset symbols and their current prices.
        """
        prices = {}
        for symbol in symbols:
            full_symbol = f"{symbol.upper()}{self.SYMBOL_PAIR}"
            prices[full_symbol] = self.get_price(full_symbol)
        return prices

    def get_ohlc(self, asset_symbol: str, interval: str, since: dt = None) -> list[dict]:
        """
        Fetches OHLC data from Binance.

        Parameters
        ----------
        asset_symbol : str
            The symbol of the asset (e.g., "BTC").
        interval : str
            The time interval for the OHLC data (e.g., "1m", "1h").
        since : datetime, optional
            The timestamp to start fetching data from.

        Returns
        -------
        list of dict
            A list of OHLC records.

        Raises
        ------
        ValueError
            If an error occurs while fetching OHLC data.
        """
        try:
            since_ms = int(since.timestamp() * 1000) if since else None
            ohlc_data = self.exchange.fetch_ohlcv(asset_symbol, timeframe=interval, since=since_ms)
            return [
                {
                    "timestamp": dt.fromtimestamp(data[0] / 1000, tz=timezone.utc),
                    "open": data[1],
                    "high": data[2],
                    "low": data[3],
                    "close": data[4],
                }
                for data in ohlc_data
            ]
        except Exception as e:
            logger.error(f"Failed to fetch OHLC data for {asset_symbol} [{interval}]. Reason: {str(e)}")
            logger.warning("Please check your internet connection or Exchange API status.")
            raise ValueError("Unable to retrieve OHLC data. Check logs for more details.")
            

    def save_ohlc(self, asset_symbol: str, interval: str, session: Session):
        """
        Saves OHLC data to the `price_history` table.

        Parameters
        ----------
        asset_symbol : str
            The symbol of the asset (e.g., "BTC").
        interval : str
            The time interval for the OHLC data (e.g., "1h").
        session : sqlalchemy.orm.Session
            The database session.

        Raises
        ------
        Exception
            If an error occurs while saving OHLC data.
        """
        logger.info(f"Saving OHLC for {asset_symbol} with interval {interval}")
        try:
            full_symbol = f"{asset_symbol}{self.SYMBOL_PAIR}"
            last_record = session.query(func.max(PriceHistory.timestamp)).filter(
                PriceHistory.asset_symbol == full_symbol,
                PriceHistory.interval == interval
            ).scalar()

            last_record = dt.now(timezone.utc) - timedelta(days=1) if last_record is None else last_record

            candles = self.get_ohlc(full_symbol, interval, since=last_record)

            for candle in candles:
                existing_candle = session.query(PriceHistory).filter_by(
                    asset_symbol=full_symbol,
                    timestamp=candle["timestamp"],
                    interval=interval,
                ).first()

                if existing_candle:
                    existing_candle.open = candle["open"]
                    existing_candle.high = max(existing_candle.high, candle["high"])
                    existing_candle.low = min(existing_candle.low, candle["low"])
                    existing_candle.close = candle["close"]
                else:
                    price_record = PriceHistory(
                        asset_symbol=full_symbol,
                        timestamp=candle["timestamp"],
                        interval=interval,
                        open=candle["open"],
                        high=candle["high"],
                        low=candle["low"],
                        close=candle["close"],
                    )
                    session.add(price_record)
                session.commit()

            logger.info(f"Successfully saved OHLC data for {asset_symbol} ({interval}).")

        except Exception as ve:
            logger.error(f"Error saving OHLC for {asset_symbol} [{interval}]: {str(ve)}")
        except Exception as e:
            logger.critical(f"Critical failure while saving OHLC for {asset_symbol}: {str(e)}")
            raise
