"""
manager.client.py

This module contains the Stoa class, which is a core component of our package.
The Stoa class offers functionality for fetching, signing, authenticating, and
ordering messages, which are essential operations for communication and data
exchange within our system.
"""

from typing import Dict, List, Literal, Optional, Union

import pandas as pd

from ..authentication import oauth2, rest
from ..fetch import fetch
from ..order import order
from ..sign import sign
from ..utils.logger import LOGGER
from ..utils.decorators import ensure_authenticated


class StoaClient:
    """
    The Stoa class provides methods for handling messages within our system.
    These methods include operations for fetching, signing, authenticating,
    and ordering messages.
    """

    def __init__(
        self,
        authentication: Literal["rest", "oauth2"],
        product_group_name: str,
        product_name: str,
        workspace: Literal["apps", "cart"],
        owner_id: str,
        version: str = "1.0",
        offset: int = 0,
        limit: int = 20,
        ascending: bool = False,
        email: Optional[str] = None,
        password: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
    ) -> None:
        """
        Constructor for the Stoa class. Initializes a new instance of the
        Stoa class.

        :param authentication: The authentication method to use.
        :param product_group_name: The name of the product group.
        :param product_name: The name of the product.
        :param workspace: The workspace where the product is located.
        :param owner_id: The ID of the owner of the product.
        :param version: The version of the product (default: "1.0").
        :param offset: The offset for pagination (default: 0).
        :param limit: The limit for pagination (default: 20).
        :param ascending: Whether to sort in ascending order (default: False).
        :param email: The email for authentication (default: None).
        :param password: The password for authentication (default: None).
        :param client_id: The client ID for authentication (default: None).
        :param client_secret: The client secret for authentication (default: None).
        """
        # Validate input parameters
        if not 0 <= offset:
            raise ValueError("Offset must be greater than or equal to 0")
        if not 0 < limit <= 20:
            raise ValueError("Limit must be less than or equal to 20")

        self.authentication = authentication
        self.product_group_name = product_group_name
        self.product_name = product_name
        self.workspace = workspace
        self.owner_id = owner_id
        self.version = version
        self.offset = offset
        self.limit = limit
        self.ascending = ascending
        self.email = email
        self.password = password
        self.client_id = client_id
        self.client_secret = client_secret

        self._token = None
        self._order_ids: List = []
        self._signatures: Dict = {}

    @property
    def token(self) -> str:
        """
        Token getter that retrieves the current access token.

        :return: The access token.
        :raises ValueError: If the access token is missing.
        """
        if not self._token:
            raise ValueError("Authentication token is missing.")
        return self._token

    @token.setter
    def token(self, value) -> None:
        """
        Token setter that sets the access token with
        additional validation or logging.

        :param value: The access token to set.
        :raises ValueError: If the access token is empty.
        """
        if not value:
            raise ValueError("Cannot set an empty access token.")
        self._token = value

    @property
    def order_ids(self) -> List[str]:
        """
        Order IDs getter that retrieves the current list of order IDs.

        :return: List of order IDs.
        :raises ValueError: If no order IDs are found.
        """
        if not self._order_ids:
            raise ValueError("No order IDs found.")
        return self._order_ids

    @order_ids.setter
    def order_ids(self, value: List) -> None:
        """
        Order IDs setter that sets the list of order IDs
        with additional validation or logging.

        :param value: List of order IDs.
        :raises ValueError: If the order IDs are not a list.
        """
        if not isinstance(value, list):
            raise ValueError("Order ID's must be a list.")

        if not value:
            raise ValueError("Cannot set an empty list of order IDs.")

        self._order_ids = value

    @property
    def signatures(self) -> Dict:
        """
        Signatures getter that retrieves the current dictionary of signatures.

        :return: Dictionary of signatures.
        :raises ValueError: If no signatures are found.
        """
        if not self._signatures:
            raise ValueError("No signatures found.")
        return self._signatures

    @signatures.setter
    def signatures(self, value: Dict) -> None:
        """
        Signatures setter that sets the dictionary of signatures
        with additional validation or logging.

        :param value: Dictionary of signatures.
        :raises ValueError: If the signatures are not a dictionary.
        """
        if not isinstance(value, dict):
            raise ValueError("signatures must be a dictionary.")

        if not value:
            raise ValueError("Cannot set an empty dictionary of signatures.")

        self._signatures = value

    def authenticate(self) -> None:
        """
        Authenticates a message to verify its origin. This method is used to
        check if a message came from a trusted source before it is processed
        by the system.

        :return: The access token for the authenticated request.
        :rtype: str
        :raises NotImplementedError: If the authentication method is invalid.

        **example**::
            >>> stoa = StoaClient(**params)
            >>> stoa.authenticate()
            >>> assert stoa.token
        """
        LOGGER.info("Authenticating request...")

        if self.authentication not in ["rest", "oauth2"]:
            raise NotImplementedError("Invalid authentication method")

        if self.authentication == "rest":

            if not self.email or not self.password:
                raise ValueError(
                    "Email and password are required for REST authentication",
                )

            self.token = rest(
                email=self.email,
                password=self.password,
            )

        if self.authentication == "oauth2":

            if not self.client_id or not self.client_secret:
                raise ValueError(
                    "Client ID and Client Secret are required for OAuth2 authentication",
                )
            self.token = oauth2(
                client_id=self.client_id,
                client_secret=self.client_secret,
            )

    def is_authenticated(self) -> bool:
        """
        Checks if a message is authenticated. This method is used to verify
        that a message has been authenticated before it is processed by the
        system.

        :return: True if the message is authenticated, False otherwise.
        :rtype: bool

        **example**::
            >>> stoa = StoaClient(**params)
            >>> stoa.authenticate()
            >>> assert stoa.is_authenticated()
        """
        try:
            return self.token is not None
        except ValueError:
            return False

    @ensure_authenticated
    def order(self) -> List[str]:
        """
        Orders a message based on predefined rules. This method is used to
        sort or arrange messages according to certain criteria before they
        are processed by the system.

        :return: Ordered keys.
        :rtype: List
        :raises ValueError: If the workspace is invalid.

        **example**::
            >>> stoa = StoaClient(**params)
            >>> stoa.order()
            >>> assert stoa.order_ids
        """
        LOGGER.info("Creating order from request...")

        if self.workspace not in ["apps", "cart"]:
            raise ValueError("Invalid workspace.")

        self.order_ids = order(
            token=self.token,
            params={
                "product_group_name": self.product_group_name,
                "product_name": self.product_name,
                "workspace": self.workspace,
                "owner_id": self.owner_id,
                "version": self.version,
                "offset": self.offset,
                "limit": self.limit,
                "ascending": self.ascending,
            },
        )
        LOGGER.info(f"({len(self.order_ids)}) orders created")
        return self.order_ids

    @ensure_authenticated
    def sign(self) -> Dict:
        """
        Signs a message to ensure its integrity and authenticity. This method
        is used to add a layer of security to our messages, making sure they
        are not tampered with during transit.

        :return: The pre-signed URLs for the messages.
        :rtype: Dict
        :raises ValueError: If the order IDs are missing.

        **example**::
            >>> stoa = StoaClient(**params)
            >>> stoa.order()
            >>> stoa.sign()
            >>> assert stoa.signatures
        """
        LOGGER.info(f"Signing {len(self.order_ids)} orders...")
        signatures = {}
        for id in self.order_ids:
            signatures[id] = sign(
                token=self.token,
                params={"key": id},
            )
        self.signatures = signatures
        return self.signatures

    def fetch(
        self,
        format: Literal["json", "dataframe"],
    ) -> Union[List[Dict], pd.DataFrame]:
        """
        Fetches a message from a predefined source. This method is responsible
        for retrieving messages that are to be processed by the system.

        :param format: The format in which to return the fetched data.
        :return: The fetched data in the specified format.
        :rtype: List[Dict]
        :raises ValueError: If the format is invalid.

        **example**::
            >>> stoa = StoaClient(**params)
            >>> stoa.fetch(format="json")
        """
        LOGGER.info(
            f"Fetching product: {self.product_name} | {self.owner_id}...",
        )
        if format not in ["json", "dataframe"]:
            raise ValueError("Invalid format")

        self.order()
        self.sign()
        dataframe = fetch(
            pre_signed_urls=self.signatures,
        )

        if format == "json":
            return dataframe.to_dict(orient="records")
        elif format == "dataframe":
            return dataframe
