"""
This module is designed to facilitate sending order requests to
the Stoa API, allowing for the automated ordering of data or
services provided by the Stoa platform.

It utilizes the `order` function to communicate with the Stoa API,
sending order requests based on specified parameters and an
authentication token. The function is designed to work in different
environments (development and production) by selecting the appropriate
API endpoint.

The `order` function returns the response from the Stoa API as a
JSON object, which typically includes details about the order
that was placed.

Dependencies:
- requests: For making HTTP requests to the Stoa API.
- os: For reading environment variables to determine the running environment.
- utils.exceptions: For enriching HTTP exceptions with more context.
- utils.logger: For logging information about the order request and its outcome.

**Example Usage**::

    from ds_stoa.order import order

    # Authentication token and parameters for the order
    token = "your_auth_token"
    params = {
        "product_group_name": "your_product_group_name",
        "product_name": "your_product_name",
        "workspace": "your_workspace",
        "owner_id": "your_owner_id",
        "version": "1.0",
        "offset": "0",
        "limit": "20",
        "ascending": "False",
    }

    # Send an order request
    order_ids = order(token=token, params=params)
    print(order_ids)
"""

import os
import requests
from typing import Dict, List

from ..utils.exceptions import enrich_http_exception
from ..utils.logger import LOGGER

BUILDING_MODE = os.getenv("BUILDING_MODE", default="dev")


def order(token: str, params: Dict) -> List[str]:
    """
    Send order request to Stoa API.

    :param token: Authentication token required for the API request.
    :param params: Parameters for the order request, such as product ID and quantity.
    :return: A dictionary containing the response from the Stoa API.

    **Example**::

            >>> order(token=token, params=params)
            ["12345.snappy.parquet", "67890.snappy.parquet"]
    """
    url = {
        "dev": "https://fmdp.io/api/stoa-dev/v2/order/",
        "prod": "https://fmdp.io/api/stoa/v2/order/",
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

    LOGGER.info("Successfully ordered...")
    return body
