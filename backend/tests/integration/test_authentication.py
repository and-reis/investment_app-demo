# -*- coding: utf-8 -*-
"""
Integration tests for authentication endpoints.

This module contains tests to validate user authentication via token, 
including URL-based tokens, headers, and invalid scenarios.

Created on Thu Dec 2 20:35:03 2024

@author: Derson
"""

import os
import requests
from app.services.user import UserService
from app.schemas.user import UserCreate

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")


def test_auth_with_url_token(cicd_user):
    """
    Validates authentication using a token passed as a URL parameter.

    Parameters
    ----------
    cicd_user : User
        A pre-existing user fixture with a valid token.

    Assertions
    ----------
    - Ensures the request returns a 200 status code.
    - Confirms that the authenticated user's email matches the expected value.
    """
    response = requests.get(f"{BASE_URL}/user/get_userdata?token={cicd_user.token}")
    assert response.status_code == 200
    assert response.json()["email"] == cicd_user.email


def test_auth_with_authorization_header(cicd_user):
    """
    Validates authentication using a token passed in the Authorization header.

    Parameters
    ----------
    cicd_user : User
        A pre-existing user fixture with a valid token.

    Assertions
    ----------
    - Ensures the request returns a 200 status code.
    - Confirms that the authenticated user's email matches the expected value.
    """
    headers = {"Authorization": f"Bearer {cicd_user.token}"}
    response = requests.get(f"{BASE_URL}/user/get_userdata", headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == cicd_user.email


def test_auth_with_invalid_token():
    """
    Validates authentication with an invalid token.

    Assertions
    ----------
    - Ensures the request returns a 401 status code.
    - Confirms the response contains the expected error message for an invalid token.
    """
    response = requests.get(f"{BASE_URL}/user/get_userdata?token=invalid_token")
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token or inactive user."}


def test_auth_missing_token():
    """
    Validates authentication without providing a token.

    Assertions
    ----------
    - Ensures the request returns a 400 status code.
    - Confirms the response contains the expected error message for a missing token.
    """
    response = requests.get(f"{BASE_URL}/user/get_userdata")
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Token not provided. Use 'Authorization: Bearer <token> or pass the token in the URL as ?token=<token>."
    }
