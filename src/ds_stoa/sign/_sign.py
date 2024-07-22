"""
Module for pre-signing URLs for fetching data from GraspDP datalake.

This module provides a function to generate pre-signed URLs for securely
accessing data stored in the GraspDP datalake. It uses an authentication
token and request parameters to request a pre-signed URL from the Stoa service,
which can then be used to fetch data without further authentication.

The `sign` function supports different environments (development and production)
by selecting the appropriate URL to request the pre-signed URL from.

Dependencies:
- **requests**: For making HTTP requests to the Stoa service.
- **os**: For reading environment variables to determine the running environment.
- **utils.exceptions**: For enriching exceptions with more context.
- **utils.logger**: For logging information and errors.

**Example Usage**::

    from ds_stoa.sign import sign

    # Authentication token and parameters for the request
    token = "your_auth_token"
    params = {"key": "12345"}

    # Generate a pre-signed URL
    pre_signed_url = sign(token=token, params=params)
    print(pre_signed_url)
"""

import os
from typing import Dict

import requests

from ..utils.exceptions import enrich_http_exception
from ..utils.logger import LOGGER

BUILDING_MODE = os.getenv("BUILDING_MODE", default="dev")


def sign(token: str, params: Dict) -> str:
    """
    Generate a pre-signed URL for accessing data in the
    GraspDP datalake.

    :param token: Authentication token required for
                  generating the pre-signed URL.
    :param params: Parameters for the request, typically including
                   identifiers for the data to be accessed.
    :return: A string containing the pre-signed URL.
    :raises ValueError: If the pre-signed URL is not found.

    **Example**::
            >>> sign(token=token, params=params)
            "https://fmdp.io/stoa-dev/sign/12345"
    """
    url = {
        "dev": "https://fmdp.io/api/stoa-dev/v2/sign/",
        "prod": "https://fmdp.io/api/stoa/v2/sign/",
    }
    url = url[BUILDING_MODE]

    try:
        response = requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            },
            params=params,
            timeout=60,
        )
        response.raise_for_status()

    except requests.HTTPError as exc:
        enrich_http_exception(exc=exc)
        raise exc

    body = response.json()
    url = body.get("url")

    if not url:
        LOGGER.error("pre-signed URL not found.")
        raise ValueError("pre-signed URL not found.")

    LOGGER.info("Successfully ordered...")
    return url
