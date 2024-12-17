# -*- coding: utf-8 -*-
"""
Schemas for Portfolio operations.

This module defines Pydantic schemas used for validation and serialization 
of Portfolio-related data, including buy/sell requests, summaries, and transaction details.

Created on Thu Nov 28 14:59:59 2024

@author: Derson
"""

from pydantic import BaseModel, field_validator, model_validator
from typing import Optional, Literal
from decimal import Decimal
from datetime import datetime


class PortfolioBuyRequest(BaseModel):
    """
    Schema for creating a buy request in the portfolio.

    Attributes
    ----------
    asset_symbol : str
        The symbol of the asset to buy (e.g., "BTC").
    trade_type : Literal["buy"]
        Fixed value indicating the type of trade ("buy").
    amount_val : Decimal
        Total amount to be invested by the user.

    Methods
    -------
    validate_positive(cls, value)
        Ensures the provided amount is greater than zero.
    """
    asset_symbol: str
    trade_type: Literal["buy"]
    amount_val: Decimal

    @field_validator("amount_val")
    def validate_positive(cls, value):
        if value <= 0:
            raise ValueError("The value must be greater than zero.")
        return value


class PortfolioBuyRequestInternal(PortfolioBuyRequest):
    """
    Internal schema for processing a buy request.

    Attributes
    ----------
    user_id : int
        ID of the user making the request.
    """
    user_id: int


class PortfolioSellRequest(BaseModel):
    """
    Schema for creating a sell request in the portfolio.

    Attributes
    ----------
    asset_symbol : str
        The symbol of the asset to sell (e.g., "BTC").
    trade_type : Literal["sell"]
        Fixed value indicating the type of trade ("sell").
    perc_withdraw : Optional[int]
        Percentage of the asset to withdraw (0 to 100).
    qty : Optional[Decimal]
        Quantity of the asset to sell.

    Methods
    -------
    validate_withdraw_or_qty(self)
        Ensures that either 'qty' or 'perc_withdraw' is provided.
    """
    asset_symbol: str
    trade_type: Literal["sell"]
    perc_withdraw: Optional[int] = None
    qty: Optional[Decimal] = None

    @model_validator(mode="after")
    def validate_withdraw_or_qty(self):
        if not self.perc_withdraw and not self.qty:
            raise ValueError("Provide 'qty' or 'perc_withdraw' to execute the sell request.")
        if self.perc_withdraw and (self.perc_withdraw < 0 or self.perc_withdraw > 100):
            raise ValueError("'perc_withdraw' must be between 0 and 100.")
        return self


class PortfolioSellRequestInternal(PortfolioSellRequest):
    """
    Internal schema for processing a sell request.

    Attributes
    ----------
    user_id : int
        ID of the user making the request.
    """
    user_id: int


class PortfolioSummary(BaseModel):
    """
    Schema for summarizing portfolio details.

    Attributes
    ----------
    asset_symbol : str
        The symbol of the asset.
    total_qty : float
        Total quantity of the asset in the portfolio.
    total_value : float
        Total value of the asset in the portfolio.
    total_fees : float
        Total fees paid for transactions involving this asset.
    """
    asset_symbol: str
    total_qty: float
    total_value: float
    total_fees: float


class PortfolioPnLResponse(BaseModel):
    """
    Schema for returning Profit and Loss (PnL) details.

    Attributes
    ----------
    asset_symbol : str
        The symbol of the asset.
    total_invested : Decimal
        Total amount invested in the asset.
    total_received : Decimal
        Total amount received from selling the asset.
    current_qty : Decimal
        Current quantity of the asset held.
    current_price : Decimal
        Current market price of the asset.
    pnl : Decimal
        The profit or loss for the asset.
    """
    asset_symbol: str
    total_invested: Decimal
    total_received: Decimal
    current_qty: Decimal
    current_price: Decimal
    pnl: Decimal


class PortfolioTransactionResponse(BaseModel):
    """
    Schema for returning portfolio transaction details.

    Attributes
    ----------
    transaction_id : int
        Unique identifier of the transaction.
    user_id : int
        ID of the user associated with the transaction.
    asset_symbol : str
        The symbol of the traded asset.
    trade_type : str
        Type of the trade ("buy" or "sell").
    qty : Decimal
        Quantity of the asset traded.
    net_val : Decimal
        Net value of the transaction after fees.
    price : Decimal
        Price per unit of the asset at the time of the transaction.
    fee : Decimal
        Fee applied to the transaction.
    trade_at : datetime
        Timestamp of the transaction.
    """
    transaction_id: int
    user_id: int
    asset_symbol: str
    trade_type: str
    qty: Decimal
    net_val: Decimal
    price: Decimal
    fee: Decimal
    trade_at: datetime

    model_config = {"from_attributes": True}