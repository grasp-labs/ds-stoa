"""
Test Module for order
-------------------------------------------
Test cases for order module.
"""

from unittest import TestCase, mock

from requests import HTTPError


from src.ds_stoa.order import order


class TestOrder(TestCase):
    def setUp(self) -> None:
        """
        Setup for the test cases.
        """
        self.token = "my_token"
        self.params = {
            "product_group_name": "my_product_group_name",
            "product_name": "my_product_name",
            "workspace": "my_workspace",
            "owner_id": "my_owner_id",
            "version": "1.0",
            "offset": "0",
            "limit": "20",
            "ascending": False,
        }

    @mock.patch("src.ds_stoa.order._order.requests.get")
    def test_order(self, _post) -> None:
        """
        Test case for order function.
        """
        # Setup
        _response = mock.Mock()
        _response.json.return_value = [
            "12345.snappy.parquet",
            "67890.snappy.parquet",
        ]
        _response.status_code = 200

        _post.return_value = _response

        # Exercise
        order_ids = order(
            self.token,
            self.params,
        )

        # Asserts
        self.assertEqual(
            order_ids,
            ["12345.snappy.parquet", "67890.snappy.parquet"],
        )

    def test_invalid_order(self) -> None:
        """
        Test case for invalid authentication.
        """
        # Exercise & Asserts
        with self.assertRaises(HTTPError) as exc:
            order(
                self.token,
                self.params,
            )

        # Asserts
        self.assertEqual(
            exc.exception.response.status_code,
            401,
        )
