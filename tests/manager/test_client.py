"""
Test Module for Manager
-----------------------
Test cases for the Manager class.
"""

from unittest import TestCase, mock

import pandas as pd
from requests import HTTPError

from src.ds_stoa.manager import StoaClient


class TestManager(TestCase):

    def setUp(self) -> None:
        self.stoa = StoaClient(
            authentication="rest",
            product_group_name="product_group_name",
            product_name="product_name",
            workspace="cart",
            owner_id="owner_id",
            email="email",
            password="password",
        )

    def test_offset_limit(self) -> None:
        """
        Test case for the offset and limit properties.
        """
        # Setup, Exercise & Asserts
        with self.assertRaises(ValueError):
            StoaClient(
                authentication="rest",
                product_group_name="product_group_name",
                product_name="product_name",
                workspace="cart",
                owner_id="owner_id",
                email="email",
                password="password",
                offset=-1,
            )

        # Setup, Exercise & Asserts
        with self.assertRaises(ValueError):
            StoaClient(
                authentication="rest",
                product_group_name="product_group_name",
                product_name="product_name",
                workspace="cart",
                owner_id="owner_id",
                email="email",
                password="password",
                limit=-1,
            )

    def test_token(self) -> None:
        """
        Test case for the token property.
        """
        # Setup, Exercise & Asserts
        with self.assertRaises(ValueError):
            self.stoa.token = None

    def test_order_ids(self) -> None:
        """
        Test case for the order_ids property.
        """
        # Setup, Exercise & Asserts
        with self.assertRaises(ValueError):
            self.stoa.order_ids

        # Setup, Exercise & Asserts
        with self.assertRaises(ValueError):
            self.stoa.order_ids = None

        # Setup, Exercise & Asserts
        with self.assertRaises(ValueError):
            self.stoa.order_ids = []

    def test_signatures(self) -> None:
        """
        Test case for the signatures property.
        """
        # Setup, Exercise & Asserts
        with self.assertRaises(ValueError):
            self.stoa.signatures

        # Setup, Exercise & Asserts
        with self.assertRaises(ValueError):
            self.stoa.signatures = None

        # Setup, Exercise & Asserts
        with self.assertRaises(ValueError):
            self.stoa.signatures = {}

    def test_no_credentials(self) -> None:
        """
        Test case for missing email and password.
        """
        # Setup, Exercise & Asserts
        with self.assertRaises(ValueError):
            stoa = StoaClient(
                authentication="rest",
                product_group_name="product_group_name",
                product_name="product_name",
                workspace="cart",
                owner_id="owner_id",
            )
            stoa.authenticate()

        # Setup, Exercise & Asserts
        with self.assertRaises(ValueError):
            stoa = StoaClient(
                authentication="oauth2",
                product_group_name="product_group_name",
                product_name="product_name",
                workspace="cart",
                owner_id="owner_id",
            )
            stoa.authenticate()

    @mock.patch("src.ds_stoa.manager.client.rest")
    def test_rest_authenticated(self, _rest) -> None:
        """
        Test case for rest-auth authentication.
        """
        # Setup
        self.stoa.authentication = "rest"
        _rest.return_value = "token"

        # Exercise
        self.stoa.authenticate()

        # Asserts
        self.assertEqual(
            self.stoa.token,
            "token",
        )
        _rest.assert_called_once_with(
            email="email",
            password="password",
        )

    @mock.patch("src.ds_stoa.manager.client.oauth2")
    def test_oauth2_authenticated(self, _oauth2) -> None:
        """
        Test case for Oauth2.0 authentication.
        """
        # Setup
        self.stoa.authentication = "oauth2"
        self.stoa.client_id = "client_id"
        self.stoa.client_secret = "client_secret"
        _oauth2.return_value = "token"

        # Exercise
        self.stoa.authenticate()

        # Asserts
        self.assertEqual(
            self.stoa.token,
            "token",
        )
        _oauth2.assert_called_once_with(
            client_id="client_id",
            client_secret="client_secret",
        )

    def test_not_authenticated(self) -> None:
        """
        Test case for invalid authentication.
        """
        # Setup, Exercise & Asserts
        with self.assertRaises(HTTPError):
            self.stoa.authenticate()

    def test_not_implemented(self) -> None:
        """
        Test case for invalid authentication method.
        """
        # Setup, Exercise & Asserts
        self.stoa.authentication = "invalid"
        with self.assertRaises(NotImplementedError):
            self.stoa.authenticate()

    def test_is_authenticated(self) -> None:
        """
        Test case for the is_authenticated method.
        """
        # Exercise
        result = self.stoa.is_authenticated()

        # Asserts
        self.assertFalse(result)

    @mock.patch.object(StoaClient, "authenticate")
    def test_invalid_workspace(self, _auth) -> None:
        """
        Test case for invalid workspace.
        """
        self.stoa.token = "token"
        self.stoa.workspace = "invalid"

        # Setup, Exercise & Asserts
        with self.assertRaises(ValueError):
            self.stoa.order()

    @mock.patch("src.ds_stoa.manager.client.order")
    @mock.patch.object(StoaClient, "authenticate")
    def test_order(self, _auth, _order) -> None:
        """
        Test case for the order method.
        """
        # Setup
        self.stoa.token = "token"
        _order.return_value = ["1234", "5678"]

        # Exercise
        self.stoa.order()

        # Asserts
        self.assertEqual(self.stoa.order_ids, ["1234", "5678"])
        _order.called_once()

    @mock.patch("src.ds_stoa.manager.client.sign")
    @mock.patch.object(StoaClient, "authenticate")
    def test_sign(self, _auth, _sign) -> None:
        """
        Test case for the sign method.
        """
        # Setup
        self.stoa.token = "token"
        self.stoa.order_ids = ["1234"]
        _sign.return_value = "https://example.com/1234.parquet"

        # Exercise
        self.stoa.sign()

        # Asserts
        self.assertEqual(
            self.stoa.signatures,
            {"1234": "https://example.com/1234.parquet"},
        )
        _sign.called_once()

    @mock.patch("src.ds_stoa.manager.client.fetch")
    @mock.patch.object(StoaClient, "sign")
    @mock.patch.object(StoaClient, "order")
    @mock.patch.object(StoaClient, "authenticate")
    def test_fetch(self, _auth, _order, _sign, _fetch) -> None:
        """
        Test case for the fetch method.
        """
        # Setup
        self.stoa.token = "token"
        self.stoa.order_ids = ["1234", "5678"]
        self.stoa.signatures = {
            "1234": "https://example.com/1234.parquet",
            "5678": "https://example.com/5678.parquet",
        }
        _fetch.return_value = pd.DataFrame()

        # Exercise
        dataframe = self.stoa.fetch(format="dataframe")
        data = self.stoa.fetch(format="json")

        # Asserts
        self.assertIsInstance(dataframe, pd.DataFrame)
        self.assertIsInstance(data, list)

    def test_invalid_format(self) -> None:
        """
        Test case for invalid format.
        """
        # Setup, Exercise & Asserts
        with self.assertRaises(ValueError):
            self.stoa.fetch(format="invalid")
