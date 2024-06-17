"""
Module for fetching data from GraspDP datalake.

This module provides methods for fetching data from the GraspDP datalake. The
fetch method allows users to retrieve data from the datalake based on the
pre-singed URLs provided by the Stoa API.
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
from io import BytesIO
from typing import Dict

import pandas as pd
import requests

from utils.logger import LOGGER


def fetch_url(url: str) -> BytesIO:
    """
    Fetch data from a given URL.

    :param url: str
    :return: BytesIO
    """
    response = requests.get(
        url=url,
        timeout=60,
    )
    return BytesIO(response.content)


def fetch(pre_signed_urls: Dict) -> pd.DataFrame:
    """
    Fetch data from URLs in parallel.

    :param pre_signed_urls: Dict
    :return: pd.DataFrame
    """
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {
            executor.submit(fetch_url, url): url for url in pre_signed_urls.values()
        }
        dataframes = []
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()
            except Exception as exc:
                LOGGER.error(f"{url} generated an exception: {exc}")
            else:
                df = pd.read_parquet(data)
                dataframes.append(df)
        return pd.concat(dataframes)
