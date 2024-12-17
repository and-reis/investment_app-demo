# -*- coding: utf-8 -*-
"""
Asset management endpoints.

This module provides endpoints for creating, listing, and updating assets.

Created on Sun Dec 1 16:16:19 2024

@author: Derson
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db_session
from app.models import Asset
from app.schemas.assets import AssetCreate, AssetUpdate, AssetResponse

router = APIRouter()

@router.post("/", response_model=AssetResponse, summary="Create a new asset")
def create_asset(data: AssetCreate, session: Session = Depends(get_db_session)):
    """
    Registers a new asset.

    Parameters
    ----------
    data : AssetCreate
        The data for creating a new asset.
    session : sqlalchemy.orm.Session
        The database session.

    Returns
    -------
    AssetResponse
        The details of the newly created asset.

    Raises
    ------
    HTTPException
        If the asset symbol is already registered.
    """
    existing_asset = session.query(Asset).filter_by(symbol=data.symbol).first()
    if existing_asset:
        raise HTTPException(status_code=400, detail="Asset already registered.")
    
    new_asset = Asset(**data.dict())
    session.add(new_asset)
    session.commit()
    session.refresh(new_asset)
    return new_asset


@router.get("/", response_model=list[AssetResponse], summary="List all assets")
def list_assets(session: Session = Depends(get_db_session)):
    """
    Lists all registered assets.

    Parameters
    ----------
    session : sqlalchemy.orm.Session
        The database session.

    Returns
    -------
    list[AssetResponse]
        A list of all registered assets.
    """
    return session.query(Asset).all()


@router.patch("/{symbol}", response_model=AssetResponse, summary="Update an asset")
def update_asset(symbol: str, data: AssetUpdate, session: Session = Depends(get_db_session)):
    """
    Updates the details of an existing asset.

    Parameters
    ----------
    symbol : str
        The unique symbol of the asset to update.
    data : AssetUpdate
        The fields to update for the asset.
    session : sqlalchemy.orm.Session
        The database session.

    Returns
    -------
    AssetResponse
        The updated asset details.

    Raises
    ------
    HTTPException
        If the asset symbol is not found.
    """
    asset = session.query(Asset).filter_by(symbol=symbol).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found.")
    
    for key, value in data.dict(exclude_unset=True).items():
        setattr(asset, key, value)

    session.commit()
    session.refresh(asset)
    return asset