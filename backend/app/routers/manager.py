# -*- coding: utf-8 -*-
"""
Manager-specific endpoints for client and portfolio management.

This module provides endpoints for managers to view their clients, retrieve 
summarized portfolio data, and calculate profit and loss (PnL) for their clients.

Created on Thu Nov 28 15:16:38 2024

@author: Derson
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.services.portfolio import PortfolioService
from app.models import Portfolio, User
from app.dependencies import get_current_user, get_db_session

router = APIRouter()

@router.get("/clients", response_model=List[dict], summary="List manager's clients")
def get_clients(session: Session = Depends(get_db_session), user=Depends(get_current_user)):
    """
    Retrieves a list of all clients managed by the current manager.

    Parameters
    ----------
    session : sqlalchemy.orm.Session
        The database session.
    user : dict
        The current authenticated manager.

    Returns
    -------
    list[dict]
        A list of dictionaries containing client IDs, usernames, and emails.

    Raises
    ------
    HTTPException
        If the user is not a manager.
    """
    if user["role"] != "manager":
        raise HTTPException(status_code=403, detail="Permission denied. Only managers can access this endpoint.")
    
    query = (
        session.query(User.user_id, User.username, User.email)
        .filter(User.manager_id == user["user_id"], User.role == "client")
    )
    return [dict(row._mapping) for row in query.all()]


@router.get("/clients/summary_all", response_model=List[dict], summary="Get portfolio summaries for all clients")
def get_summarized_clients_portfolios(session: Session = Depends(get_db_session), user=Depends(get_current_user)):
    """
    Retrieves a summarized view of the portfolios of all clients managed by the current manager.

    Parameters
    ----------
    session : sqlalchemy.orm.Session
        The database session.
    user : dict
        The current authenticated manager.

    Returns
    -------
    list[dict]
        A list of dictionaries containing client IDs, usernames, asset symbols, 
        total quantities, and total values.

    Raises
    ------
    HTTPException
        If the user is not a manager.
    """
    if user["role"] != "manager":
        raise HTTPException(status_code=403, detail="Permission denied. Only managers can access this endpoint.")
    
    query = (
        session.query(
            User.user_id,
            User.username,
            Portfolio.asset_symbol,
            func.abs(func.sum(func.coalesce(Portfolio.qty, 0))).label("total_qty"),
            func.abs(func.sum(func.coalesce(Portfolio.net_val, 0))).label("total_value"),
        )
        .outerjoin(Portfolio, Portfolio.user_id == User.user_id)
        .filter(User.manager_id == user["user_id"])
        .group_by(User.user_id, User.username, Portfolio.asset_symbol)
    )
    
    return [dict(row._mapping) for row in query.all()]


@router.get("/clients_pnl", response_model=List[dict], summary="Get PnL for all clients")
def get_client_pnl(session: Session = Depends(get_db_session), user=Depends(get_current_user)):
    """
    Retrieves the Profit and Loss (PnL) for all clients managed by the current manager.

    Parameters
    ----------
    session : sqlalchemy.orm.Session
        The database session.
    user : dict
        The current authenticated manager.

    Returns
    -------
    list[dict]
        A list of dictionaries containing client IDs, usernames, and their PnL data.

    Raises
    ------
    HTTPException
        If the user is not a manager.
    """
    if user["role"] != "manager":
        raise HTTPException(status_code=403, detail="Permission denied. Only managers can access this endpoint.")
    
    # Validate that the clients belong to the manager
    client_ids = (
        session.query(User.user_id, User.username)
        .filter(User.manager_id == user["user_id"], User.role == "client")
        .all()
    )

    result = [
        {
            "user_id": client._mapping["user_id"],
            "username": client._mapping["username"],
            "pnl": pnl_data,
        }
        for client in client_ids
        if (pnl_data := PortfolioService.get_pnl(client._mapping["user_id"], session))
    ]
    
    return result

@router.post("/trade_by_manager", summary="On-holding: Trade by manager")
def trade_by_manager():
    """
    Placeholder for a future feature allowing managers to trade on behalf of clients.

    Status
    ------
    On-holding: This endpoint is not yet implemented.

    Notes
    -----
    This feature will allow managers to leverage their expertise to execute trades for clients directly.

    Returns
    -------
    dict
        A message indicating the endpoint is on hold.
    """
    return {"message": "This feature is on-holding and will be implemented soon."}