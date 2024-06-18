"""
This module provides an interface for OAuth2 authentication with the Stoa API.
It encapsulates the process of obtaining an access token using the client
credentials flow, suitable for server-to-server authentication where an
application acts on its own behalf.

The module abstracts the complexities involved in the HTTP request and
response handling, error management, and environment-specific configuration.
It leverages the `requests` library for making HTTP requests and uses basic
authentication to securely transmit the client credentials.

The `oauth2` function within this module is designed to be used by
applications that require an access token to authenticate against the Stoa
API's protected endpoints. This token is obtained by presenting valid
client credentials (client ID and client secret) to the Stoa API's
OAuth2 token endpoint.

Usage of this module requires setting up the appropriate environment variable
`BUILDING_MODE` to toggle between development and production configurations.
This allows for flexible deployment and testing without code changes.

Dependencies:
- **requests**: For making HTTP requests to the OAuth2 token endpoint.
- **utils.exceptions**: For enriching HTTP exceptions with more context.
- **utils.logger**: For logging information about the authentication process and errors.

Example usage::

    from ds_stoa.authentication import oauth2

    # Obtain an access token using client credentials
    access_token = oauth2('your_client_id', 'your_client_secret')
    print(access_token)

"""

import os

import requests
from requests import auth

from ..utils.exceptions import enrich_http_exception
from ..utils.logger import LOGGER

BUILDING_MODE = os.getenv("BUILDING_MODE", default="dev")


def oauth2(client_id: str, client_secret: str) -> str:
    """
    Authenticates an application and retrieves an access token.

    :param client_id: The Client ID.
    :type client_id: str
    :param client_secret: The Client Secret.
    :type client_secret: str
    :returns: An access token indicating successful authentication.
    :rtype: str

    **Example**::

        >>> oauth2('client_id', 'client_secret')
        'access_token_value'
    """
    url = {
        "dev": "https://auth-dev.grasp-daas.com/oauth/token/",
        "prod": "https://auth.grasp-daas.com/oauth/token/",
    }
    url = url[BUILDING_MODE]

    payload = {
        "grant_type": "client_credentials",
    }

    try:
        response = requests.post(
            url,
            auth=auth.HTTPBasicAuth(
                client_id,
                client_secret,
            ),
            data=payload,
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
