"""
Module for pre-signing URLs for fetching data from GraspDP datalake.
"""

import os
from typing import Dict

import requests

from utils.exceptions import enrich_http_exception
from utils.logger import LOGGER

BUILDING_MODE = os.getenv("BUILDING_MODE", default="dev")


def sign(token: str, params: Dict) -> str:
    """
    Sign a URL with a given key.

    :param token: str
    :param key: str
    :return: str
    """
    url = {
        "dev": "https://fmdp.io/stoa-dev/sign/",
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
