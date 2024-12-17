# -*- coding: utf-8 -*-
"""
Schemas for Asset operations.

This module defines Pydantic schemas used for validation and serialization 
of Asset-related data in the application.

Created on Sun Dec 1 16:17:32 2024

@author: Derson
"""

from pydantic import BaseModel
from typing import Optional


class AssetBase(BaseModel):
    """
    Base schema for Asset objects.

    Attributes
    ----------
    name : str
        The name of the asset (e.g., "Bitcoin").
    symbol : str
        The unique symbol of the asset (e.g., "BTC").
    type : str
        The type of the asset (e.g., "cryptocurrency", "stock").
    """
    name: str
    symbol: str
    type: str


class AssetCreate(AssetBase):
    """
    Schema for creating a new Asset.

    Inherits
    --------
    AssetBase
        Base attributes required for creating an Asset.
    """
    pass


class AssetUpdate(BaseModel):
    """
    Schema for updating an existing Asset.

    Attributes
    ----------
    name : Optional[str]
        The new name of the asset.
    symbol : Optional[str]
        The new unique symbol of the asset.
    type : Optional[str]
        The new type of the asset.
    active : Optional[bool]
        The new active status of the asset.
    """
    name: Optional[str] = None
    symbol: Optional[str] = None
    type: Optional[str] = None
    active: Optional[bool] = None


class AssetResponse(BaseModel):
    """
    Schema for returning Asset details.

    Attributes
    ----------
    id : int
        Unique identifier of the asset.
    name : str
        The name of the asset.
    symbol : str
        The unique symbol of the asset.
    type : str
        The type of the asset.
    active : bool
        Indicates if the asset is active.
    """
    id: int
    name: str
    symbol: str
    type: str
    active: bool

    model_config = {"from_attributes": True}