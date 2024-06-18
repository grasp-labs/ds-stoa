"""
This module serves as the entry point for the data fetching
functionality from the GraspDP datalake.

It exposes the `fetch` function, which is designed to retrieve data from the
datalake using pre-signed URLs. This function is capable of fetching data in parallel,
significantly improving performance for large datasets.

The `fetch` function returns the data as a Pandas DataFrame, making it immediately useful
for data analysis and manipulation tasks.

**Example usage**::

    from ds_stoa.fetch import fetch

    # Example pre-signed URLs (these would be provided by your data provider)
    pre_signed_urls = {
        "dataset1": "http://example.com/path/to/dataset1.parquet",
        "dataset2": "http://example.com/path/to/dataset2.parquet",
    }

    # Fetching data and loading it into a DataFrame
    dataframe = fetch(pre_signed_urls)
    print(dataframe)
"""

from ._fetch import fetch

__all__ = ["fetch"]
