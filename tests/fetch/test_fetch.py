"""
Test Module for Fetching Data
-------------------------------------------
Test cases for the data fetching module.
"""

from unittest import TestCase, mock
from unittest.mock import MagicMock

from io import BytesIO
import pandas as pd

from src.ds_stoa.fetch._fetch import fetch, fetch_url


class TestFetch(TestCase):
    def setUp(self):
        self.pre_signed_urls = {
            "key": "http://example.com/data1.parquet",
        }
        self._dataframe = pd.DataFrame(
            {"column1": [1, 2, 3], "column2": ["a", "b", "c"]}
        )

    @mock.patch("src.ds_stoa.fetch._fetch.requests.get")
    def test_fetch_url(self, mock_get):
        """
        Test case for the fetch_url function.
        """
        # Setup
        _response = MagicMock()

        _response.content = b"mock data"
        _response.raise_for_status = MagicMock()
        mock_get.return_value = _response

        # Exercise
        response = fetch_url(
            url="http://example.com/data.parquet",
        )

        # Asserts
        self.assertIsInstance(response, BytesIO)
        self.assertEqual(response.read(), b"mock data")

    @mock.patch("src.ds_stoa.fetch._fetch.fetch_url")
    def test_fetch(self, _fetch_url):
        """
        Test case for the fetch function.
        """
        # Setup
        _buffer = BytesIO()
        self._dataframe.to_parquet(_buffer, index=False)
        _buffer.seek(0)

        _fetch_url.return_value = _buffer

        # Exercise
        dataframe = fetch(self.pre_signed_urls)

        # Asserts
        self.assertIsInstance(dataframe, pd.DataFrame)
        self.assertEqual(dataframe.shape, (3, 2))

    @mock.patch("src.ds_stoa.fetch._fetch.LOGGER.error")
    @mock.patch("src.ds_stoa.fetch._fetch.fetch_url")
    def test_fetch_error(self, _fetch_url, _logger):
        """
        Test case for the fetch function.
        """
        # Setup
        pre_signed_urls = {
            "bad_file": "http://example.com/data1.parquet",
            "good_file": "http://example.com/data2.parquet",
        }
        _buffer = BytesIO()
        self._dataframe.to_parquet(_buffer, index=False)
        _buffer.seek(0)

        _fetch_url.side_effect = [
            Exception("Test exception"),
            _buffer,
        ]

        # Exercise & Asserts
        dataframe = fetch(pre_signed_urls)

        # Asserts
        self.assertIsInstance(dataframe, pd.DataFrame)
        self.assertEqual(dataframe.shape, (3, 2))
        _logger.assert_called_once_with(
            "http://example.com/data1.parquet generated an exception: Test exception"
        )
