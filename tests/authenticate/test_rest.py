"""
Test Module for Authenticating with RestFul API
-----------------------------------------------
Test cases for the restful API authentication.
"""

from unittest import TestCase, mock

from requests import HTTPError


from src.ds_stoa.authentication import rest


class TestRestFul(TestCase):

    def setUp(self) -> None:
        self.email = "email@email.com"
        self.password = "my_password"

    @mock.patch("src.ds_stoa.authentication._rest.requests.post")
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
        access_token = rest(
            self.email,
            self.password,
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
            rest(
                self.email,
                self.password,
            )

        # Asserts
        self.assertEqual(
            exc.exception.response.status_code,
            400,
        )

    @mock.patch("src.ds_stoa.authentication._rest.requests.post")
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
            rest(
                self.email,
                self.password,
            )
