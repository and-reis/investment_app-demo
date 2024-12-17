"""
Integration tests for price service.

This module contains tests to validate the behavior of the `PriceService` methods,
including fetching current prices and OHLC data from the exchange API.

Created on Thu Dec 2 12:35:19 2024

@author: Derson
"""

from unittest.mock import patch
from app.services.prices import PriceService


# Functions to be tested
def get_current_prices_from_exchange_api():
    """
    Fetches the current price for an asset directly from the exchange API.

    Returns
    -------
    dict
        A dictionary containing the price and symbol of the asset.
    """
    symbol = "BTC"
    price_service = PriceService()
    return price_service.get_price(asset_symbol=symbol, from_api=True)


def get_prices_OHLC_from_exchange_api():
    """
    Fetches OHLC data for an asset directly from the exchange API.

    Returns
    -------
    dict
        A dictionary containing OHLC data (open, high, low, close) and the timestamp.
    """
    symbol = "BTC"
    price_service = PriceService()
    return price_service.get_ohlc(asset_symbol=symbol, interval="1d", since="2023-01-01T00:00:00Z")


# Tests
def test_get_current_prices_from_exchange_api():
    """
    Validates the behavior of `get_current_prices_from_exchange_api` with mocked API data.

    Assertions
    ----------
    - Ensures the returned response matches the mocked price and symbol.
    - Validates that the `PriceService.get_price` method is called with the correct arguments.
    """
    with patch("app.services.prices.PriceService.get_price") as mock_get_price:
        # Simulate API response
        mock_get_price.return_value = {"price": 35000, "symbol": "BTC"}

        # Execute the function
        response = get_current_prices_from_exchange_api()

        # Validations
        assert response == {"price": 35000, "symbol": "BTC"}
        mock_get_price.assert_called_once_with(asset_symbol="BTC", from_api=True)


def test_get_prices_ohlc_from_exchange_api():
    """
    Validates the behavior of `get_prices_OHLC_from_exchange_api` with mocked OHLC API data.

    Assertions
    ----------
    - Ensures the returned response contains the correct symbol and OHLC data.
    - Validates that the `PriceService.get_ohlc` method is called with the correct arguments.
    """
    with patch("app.services.prices.PriceService.get_ohlc") as mock_get_ohlc:
        # Simulate API response
        mock_get_ohlc.return_value = {
            "symbol": "BTC",
            "timestamp": "2024-01-01T00:00:00Z",
            "open": 46500,
            "high": 51000,
            "low": 43000,
            "close": 48500,
        }

        # Execute the function
        response = get_prices_OHLC_from_exchange_api()

        # Validations
        assert response["symbol"] == "BTC"
        assert response["open"] is not None
        assert response["close"] == 48500
        mock_get_ohlc.assert_called_once_with(asset_symbol="BTC", interval="1d", since="2023-01-01T00:00:00Z")
