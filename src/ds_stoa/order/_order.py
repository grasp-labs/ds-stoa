"""
Module for stoa order request.
"""

import os
import requests
from typing import Dict, List

from utils.exceptions import enrich_http_exception
from utils.logger import LOGGER

BUILDING_MODE = os.getenv("BUILDING_MODE", default="dev")


def order(token: str, params: Dict) -> List[str]:
    """
    Send order request to Stoa API.

    :param token: str
    :param params: Dict
    :return: List[str]
    """
    url = {
        "dev": "https://fmdp.io/stoa-dev/order/",
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
