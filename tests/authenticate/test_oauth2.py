"""
Test Module for Authenticating with Oauth2
-------------------------------------------
Test cases for the Oauth2.0 authentication.
"""

from unittest import TestCase, mock

from requests import HTTPError


from src.ds_stoa.authentication import oauth2


class TestOauth(TestCase):

    def setUp(self) -> None:
        self.client_id = "client_id"
        self.client_secret = "client_secret"

    @mock.patch("src.ds_stoa.authentication._oauth2.requests.post")
    def test_authenticate(self, _post) -> None:
        """
        Test case for the oauth2 function.
        """
        # Setup
        _response = mock.Mock()
        _response.json.return_value = {"access_token": "access_token_value"}
        _response.status_code = 200

        _post.return_value = _response

        # Exercise
        access_token = oauth2(
            self.client_id,
            self.client_secret,
        )

        # Asserts
        self.assertEqual(
            access_token,
            "access_token_value",
        )

    def test_invalid_authentication(self) -> None:
        """
        Test case for invalid authentication.
        """
        # Exercise & Asserts
        with self.assertRaises(HTTPError) as exc:
            oauth2(
                self.client_id,
                self.client_secret,
            )

        # Asserts
        self.assertEqual(
            exc.exception.response.status_code,
            401,
        )

    @mock.patch("src.ds_stoa.authentication._oauth2.requests.post")
    def test_no_access_token(self, _post) -> None:
        """
        Test case for the oauth2 function.
        """
        # Setup
        _response = mock.Mock()
        _response.json.return_value = {"access_token": None}
        _response.status_code = 200

        _post.return_value = _response

        # Exercise
        with self.assertRaises(ValueError):
            oauth2(
                self.client_id,
                self.client_secret,
            )
