"""
Test Module for sign
-------------------------------------------
Test cases for sign module.
"""

from unittest import TestCase, mock

from requests import HTTPError


from src.ds_stoa.sign import sign


class TestSign(TestCase):
    def setUp(self) -> None:
        """
        Setup for the test cases.
        """
        self.token = "my_token"
        self.params = {
            "key": "12345.snappy.parquet",
        }

    @mock.patch("src.ds_stoa.sign._sign.requests.get")
    def test_sign(self, _post) -> None:
        """
        Test case for sign function.
        """
        # Setup
        _response = mock.Mock()
        _response.json.return_value = {
            "url": "https://fmdp.io/stoa-dev/sign/12345",
        }
        _response.status_code = 200

        _post.return_value = _response

        # Exercise
        order_ids = sign(
            self.token,
            self.params,
        )

        # Asserts
        self.assertEqual(
            order_ids,
            "https://fmdp.io/stoa-dev/sign/12345",
        )

    def test_invalid_sign(self) -> None:
        """
        Test case for invalid authentication.
        """
        # Exercise & Asserts
        with self.assertRaises(HTTPError) as exc:
            sign(
                self.token,
                self.params,
            )

        # Asserts
        self.assertEqual(
            exc.exception.response.status_code,
            401,
        )

    @mock.patch("src.ds_stoa.sign._sign.requests.get")
    def test_no_signed_url(self, _post) -> None:
        """
        Test case for the oauth2 function.
        """
        # Setup
        _response = mock.Mock()
        _response.json.return_value = {"url": None}
        _response.status_code = 200

        _post.return_value = _response

        # Exercise
        with self.assertRaises(ValueError):
            sign(
                self.token,
                self.params,
            )
