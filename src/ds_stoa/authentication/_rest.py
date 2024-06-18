"""
This module provides an interface for RESTful authentication with the Stoa
API. It encapsulates the process of authenticating a user by their email and
password, returning an access token for successful authentication.

The module abstracts away the details involved in constructing the HTTP
request, handling the response, managing errors, and logging. It uses the
`requests` library to make HTTP POST requests and handles JSON responses.

The `rest` function within this module is designed for applications needing to
authenticate users against the Stoa API's RESTful authentication endpoint.
This function returns an access token that can be used to authorize subsequent
API requests.

Usage of this module requires setting the `BUILDING_MODE` environment variable
to switch between development and production environments. This facilitates
easy testing and deployment without needing to alter the codebase.

Dependencies:
- **requests**: For making HTTP requests to the authentication endpoint.
- **utils.exceptions**: For enriching HTTP exceptions with additional context.
- **utils.logger**: For logging the authentication process and any errors that occur.

Example usage::

    from ds_stoa.authentication import rest

    # Authenticate a user and obtain an access token
    access_token = rest('user@example.com', 'password123')
    print(access_token)
"""

import os

import requests

from ..utils.exceptions import enrich_http_exception
from ..utils.logger import LOGGER


BUILDING_MODE = os.getenv("BUILDING_MODE", default="dev")


def rest(email: str, password: str) -> str:
    """
    Authenticates a user and retrieves an access token.

    :param email: The email of the user.
    :type email: str
    :param password: The password of the user.
    :type password: str
    :returns: An access token indicating successful authentication.
    :rtype: str

    **Example**::

        >>> rest('user@example.com', 'secret')
        'access_token_value'
    """
    url = {
        "dev": "https://auth-dev.grasp-daas.com/rest-auth/login/",
        "prod": "https://auth.grasp-daas.com/rest-auth/login/",
    }
    url = url[BUILDING_MODE]

    payload = {"email": email, "password": password}
    try:
        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=60,
        )
        response.raise_for_status()

    except requests.HTTPError as exc:
        enrich_http_exception(exc=exc)
        raise exc

    body = response.json()

    access_token: str = body.get("access_token")

    if not access_token:
        LOGGER.error("Error: Access token not found.")
        raise ValueError("Access token not found.")

    LOGGER.info("Successfully authenticated...")
    return access_token
