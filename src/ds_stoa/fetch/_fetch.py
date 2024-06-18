"""
Module for fetching data from GraspDP datalake.

This module provides methods for fetching data from the GraspDP datalake. It
enables users to retrieve data efficiently using pre-signed URLs provided by
the Stoa API. The primary functionality is encapsulated in the `fetch` function,
which retrieves data in parallel from multiple URLs and returns a consolidated
Pandas DataFrame.

`Dependencies`:
- **pandas**: For handling and consolidating data into DataFrames.
- **requests**: For making HTTP requests to fetch data from URLs.
- **concurrent.futures**: For parallel execution of data fetching.
- **utils.logger**: For logging errors and information.

`Example usage`::

    pre_signed_urls = {
        "file1": "http://example.com/data1.parquet",
        "file2": "http://example.com/data2.parquet",
    }
    dataframe = fetch(pre_signed_urls)
    print(dataframe)
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
from io import BytesIO
from typing import Dict

import pandas as pd
import requests

from ..utils.logger import LOGGER


def fetch_url(url: str) -> BytesIO:
    """
    Fetch data from a given URL and return it as a BytesIO object.

    :param url: The URL to fetch the data from.
    :type url: str
    :return: A BytesIO object containing the fetched data.
    :rtype: BytesIO

    **Example**::

        >>> fetch_url("http://example.com/data.parquet")
    """
    response = requests.get(
        url=url,
        timeout=60,
    )
    response.raise_for_status()
    return BytesIO(response.content)


def fetch(pre_signed_urls: Dict) -> pd.DataFrame:
    """
    Fetch data from a collection of pre-signed URLs in
    parallel and consolidate into a single DataFrame.

    :param pre_signed_urls: A dictionary where keys are identifiers and values are pre-signed URLs.
    :type pre_signed_urls: Dict[str, str]
    :return: A consolidated Pandas DataFrame containing data from all fetched URLs.
    :rtype: pd.DataFrame

    **Example**::

        pre_signed_urls = {
            "file1": "http://example.com/data1.parquet",
            "file2": "http://example.com/data2.parquet",
        }
        dataframe = fetch(pre_signed_urls)
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
                continue
            df = pd.read_parquet(data)
            dataframes.append(df)
        return pd.concat(dataframes)
