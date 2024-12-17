# -*- coding: utf-8 -*-
"""
Portfolio management endpoints.

This module provides endpoints for managing portfolio transactions, 
including buying and selling assets, retrieving portfolio summaries, 
and calculating profit and loss (PnL).

Created on Thu Nov 28 15:05:23 2024

@author: Derson
"""

import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.dependencies import get_db_session
from app.services.portfolio import PortfolioService
from app.schemas.portfolio import (
    PortfolioBuyRequest,
    PortfolioSellRequest,
    PortfolioTransactionResponse,
    PortfolioSummary,
    PortfolioPnLResponse,
)
from app.dependencies import get_current_user

logging.basicConfig(level=logging.DEBUG)
router = APIRouter()


@router.post("/buy", response_model=PortfolioTransactionResponse, summary="Create a buy transaction")
def create_buy_transaction(
    data: PortfolioBuyRequest, 
    session: Session = Depends(get_db_session), 
    user=Depends(get_current_user),
):
    """
    Adds a buy transaction to the current user's portfolio.

    Parameters
    ----------
    data : PortfolioBuyRequest
        The buy transaction details.
    session : sqlalchemy.orm.Session
        The database session.
    user : dict
        The current authenticated user.

    Returns
    -------
    PortfolioTransactionResponse
        The details of the created transaction.

    Raises
    ------
    HTTPException
        If the transaction cannot be processed due to validation errors.
    """
    try:
        transaction_data = data.model_dump()
        transaction_data["user_id"] = user["user_id"]
        return PortfolioService.add_transaction(transaction_data, session)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/sell", response_model=PortfolioTransactionResponse, summary="Create a sell transaction")
def create_sell_transaction(
    data: PortfolioSellRequest, 
    session: Session = Depends(get_db_session), 
    user=Depends(get_current_user),
):
    """
    Adds a sell transaction to the current user's portfolio.

    Parameters
    ----------
    data : PortfolioSellRequest
        The sell transaction details.
    session : sqlalchemy.orm.Session
        The database session.
    user : dict
        The current authenticated user.

    Returns
    -------
    PortfolioTransactionResponse
        The details of the created transaction.

    Raises
    ------
    HTTPException
        If the transaction cannot be processed due to validation errors.
    """
    try:
        transaction_data = data.model_dump()
        transaction_data["user_id"] = user["user_id"]
        return PortfolioService.add_transaction(transaction_data, session)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/pnl", response_model=List[PortfolioPnLResponse], summary="Get profit and loss (PnL)")
def get_pnl(
    session: Session = Depends(get_db_session), 
    user=Depends(get_current_user),
):
    """
    Calculates the Profit and Loss (PnL) based on the complete transaction history.

    Parameters
    ----------
    session : sqlalchemy.orm.Session
        The database session.
    user : dict
        The current authenticated user.

    Returns
    -------
    list[PortfolioPnLResponse]
        The PnL details for each asset.

    Raises
    ------
    HTTPException
        If the PnL cannot be calculated due to an internal error.
    """
    try:
        pnl_result = PortfolioService.get_pnl(user["user_id"], session)
        return pnl_result
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        raise HTTPException(status_code=400, detail="Unable to fetch PnL.")


@router.get("/summary", response_model=List[PortfolioSummary], summary="Get portfolio summary")
def get_portfolio_summary(
    session: Session = Depends(get_db_session), 
    user=Depends(get_current_user),
):
    """
    Retrieves a summary of the current user's portfolio.

    Parameters
    ----------
    session : sqlalchemy.orm.Session
        The database session.
    user : dict
        The current authenticated user.

    Returns
    -------
    list[PortfolioSummary]
        The portfolio summary, including total quantities, values, and fees for each asset.

    Raises
    ------
    HTTPException
        If the summary cannot be retrieved due to an internal error.
    """
    logging.debug(f"Current user: {user}")
    try:
        summary = PortfolioService.get_summary(user["user_id"], session)
        logging.debug(f"Returned summary: {summary}")
        return summary
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error.")
