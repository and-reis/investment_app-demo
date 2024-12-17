# -*- coding: utf-8 -*-
"""
Service layer for Portfolio operations.

This module provides business logic for managing portfolio transactions,
including buying, selling, summarizing portfolio details, and calculating
profit and loss (PnL).

Created on Thu Nov 28 15:01:11 2024

@author: Derson
"""

from sqlalchemy.orm import Session
from sqlalchemy.sql import func, case
from app.models import Portfolio
from app.schemas.portfolio import PortfolioBuyRequestInternal, PortfolioSellRequestInternal
from app.services.wallet import WalletService
from app.services.prices import PriceService
from typing import List
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)


class PortfolioService:
    """
    Service class for managing portfolio-related operations.

    Attributes
    ----------
    FEE_RATE : Decimal
        Default fixed transaction fee rate (0.01%).
    MINIMUM_INVESTMENT : Decimal
        Minimum investment amount for buy transactions.
    """
    FEE_RATE = Decimal("0.0001")
    MINIMUM_INVESTMENT = Decimal("10.0")

    @staticmethod
    def add_transaction(data: dict, session: Session) -> Portfolio:
        """
        Registers a buy or sell transaction in the portfolio.

        Parameters
        ----------
        data : dict
            Transaction data, including trade type, asset symbol, and amount.
        session : sqlalchemy.orm.Session
            The database session.

        Returns
        -------
        Portfolio
            The registered portfolio transaction.

        Raises
        ------
        ValueError
            If the transaction type is invalid.
        """
        if data.get("trade_type") == "buy":
            data_trade = PortfolioBuyRequestInternal(**data)
            return PortfolioService._handle_buy(data_trade, session, PortfolioService.FEE_RATE)

        elif data.get("trade_type") == "sell":
            data_trade = PortfolioSellRequestInternal(**data)
            return PortfolioService._handle_sell(data_trade, session, PortfolioService.FEE_RATE)

        raise ValueError("Invalid transaction type. Use 'buy' or 'sell'.")

    @staticmethod
    def _handle_buy(data: PortfolioBuyRequestInternal, session: Session, fee_rate: Decimal) -> Portfolio:
        """
        Handles logic for registering a buy transaction.

        Parameters
        ----------
        data : PortfolioBuyRequestInternal
            The buy request data.
        session : sqlalchemy.orm.Session
            The database session.
        fee_rate : Decimal
            The transaction fee rate.

        Returns
        -------
        Portfolio
            The registered portfolio transaction.

        Raises
        ------
        ValueError
            If the investment amount is below the minimum or exceeds the user's wallet balance.
        """
        price_service = PriceService()
        trade_price = Decimal(price_service.get_price(data.asset_symbol, session=session))

        if not trade_price:
            raise ValueError("Unable to fetch asset price.")

        amount_value = Decimal(data.amount_val)
        if amount_value < PortfolioService.MINIMUM_INVESTMENT:
            raise ValueError(f"Minimum investment amount is {PortfolioService.MINIMUM_INVESTMENT}.")

        balance = WalletService.get_balance(data.user_id, session)
        if amount_value > balance:
            raise ValueError("Insufficient wallet balance.")

        transaction_fee = amount_value * fee_rate
        net_value = amount_value - transaction_fee
        qty = net_value / trade_price

        WalletService.update_balance(data.user_id, -amount_value, session)

        full_symbol = f"{data.asset_symbol.upper()}{PriceService.SYMBOL_PAIR}"
        transaction = Portfolio(
            user_id=data.user_id,
            asset_symbol=full_symbol,
            trade_type="buy",
            qty=qty,
            net_val=net_value,
            price=trade_price,
            fee=transaction_fee,
        )
        session.add(transaction)
        session.commit()
        session.refresh(transaction)
        return transaction

    @staticmethod
    def _handle_sell(data: PortfolioSellRequestInternal, session: Session, fee_rate: Decimal) -> Portfolio:
        """
        Handles logic for registering a sell transaction.

        Parameters
        ----------
        data : PortfolioSellRequestInternal
            The sell request data.
        session : sqlalchemy.orm.Session
            The database session.
        fee_rate : Decimal
            The transaction fee rate.

        Returns
        -------
        Portfolio
            The registered portfolio transaction.

        Raises
        ------
        ValueError
            If the user lacks sufficient asset quantity or wallet balance.
        """
        price_service = PriceService()
        trade_price = Decimal(price_service.get_price(data.asset_symbol, session=session))

        if not trade_price:
            raise ValueError("Unable to fetch asset price.")

        summary = PortfolioService.get_summary(data.user_id, session)
        full_symbol = f"{data.asset_symbol.upper()}{PriceService.SYMBOL_PAIR}"
        asset_summary = next((item for item in summary if item["asset_symbol"] == full_symbol), None)

        if not asset_summary or Decimal(asset_summary["total_qty"]) <= 0:
            raise ValueError("Insufficient asset quantity for sale.")

        if data.qty:
            qty = Decimal(data.qty)
            if qty > Decimal(asset_summary["total_qty"]):
                raise ValueError(f"Insufficient quantity. Available: {asset_summary['total_qty']}.")
        elif data.perc_withdraw:
            perc = Decimal(data.perc_withdraw) / Decimal(100)
            qty = Decimal(asset_summary["total_qty"]) * perc
        else:
            raise ValueError("Specify 'qty' or 'perc_withdraw' for a sell transaction.")

        amount_value = qty * trade_price
        transaction_fee = amount_value * fee_rate
        net_value = amount_value - transaction_fee

        WalletService.update_balance(data.user_id, round(net_value, 3), session)

        transaction = Portfolio(
            user_id=data.user_id,
            asset_symbol=full_symbol,
            trade_type="sell",
            qty=-qty,
            net_val=round(-net_value, 3),
            price=trade_price,
            fee=transaction_fee,
        )
        session.add(transaction)
        session.commit()
        session.refresh(transaction)
        return transaction

    @staticmethod
    def get_summary(user_id: int, session: Session) -> List[dict]:
        """
        Fetches the user's portfolio summary.

        Parameters
        ----------
        user_id : int
            The user's ID.
        session : sqlalchemy.orm.Session
            The database session.

        Returns
        -------
        list of dict
            A list summarizing the portfolio's assets.
        """
        query = session.query(
            Portfolio.asset_symbol.label("asset_symbol"),
            func.sum(Portfolio.qty).label("total_qty"),
            case(
                (func.sum(Portfolio.qty) == 0, Decimal(0)),
                else_=func.abs(func.sum(Portfolio.net_val))
            ).label("total_value"),
            func.sum(Portfolio.fee).label("total_fees")
        ).filter(Portfolio.user_id == user_id).group_by(Portfolio.asset_symbol)

        result = query.all()
        return [
            {
                "asset_symbol": row.asset_symbol,
                "total_qty": Decimal(row.total_qty),
                "total_value": Decimal(row.total_value),
                "total_fees": Decimal(row.total_fees),
            }
            for row in result
        ]

    @staticmethod
    def get_pnl(user_id: int, session: Session) -> list[dict]:
        """
        Calculates Profit and Loss (PnL) based on the transaction history.

        Parameters
        ----------
        user_id : int
            The user's ID.
        session : sqlalchemy.orm.Session
            The database session.

        Returns
        -------
        list of dict
            A list of PnL details for each asset.
        """
        transactions = session.query(
            Portfolio.asset_symbol.label("asset_symbol"),
            func.sum(
                case((Portfolio.trade_type == "buy", Portfolio.net_val), else_=0)
            ).label("total_invested"),
            func.sum(
                case((Portfolio.trade_type == "sell", Portfolio.net_val), else_=0)
            ).label("total_received"),
            func.sum(Portfolio.qty).label("current_qty"),
        ).filter(Portfolio.user_id == user_id).group_by(Portfolio.asset_symbol).all()

        pnl_data = []
        price_service = PriceService()

        for row in transactions:
            total_invested = Decimal(row.total_invested)
            total_received = Decimal(row.total_received)
            current_qty = Decimal(row.current_qty)
            asset_symbol = row.asset_symbol

            total_received_positive = -total_received
            pnl = total_received_positive - total_invested

            current_price = Decimal(0)
            if current_qty > 0:
                current_price = Decimal(price_service.get_price(row.asset_symbol.replace('USDT', ''), session=session))
                pnl += current_price * current_qty

            pnl_data.append({
                "asset_symbol": asset_symbol,
                "total_invested": total_invested,
                "total_received": -total_received,
                "current_qty": current_qty,
                "current_price": current_price,
                "pnl": pnl,
            })

        return pnl_data