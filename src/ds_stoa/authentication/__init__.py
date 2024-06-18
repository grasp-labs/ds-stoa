"""
This module provides authentication and RESTful API interaction capabilities for the Stoa API.

It includes two primary functions:

- **oauth2**: For obtaining OAuth2 authentication tokens necessary for secure API access. This function uses client ID and client secret to authenticate.
- **rest**: For making authenticated RESTful API requests to various endpoints within the Stoa API. This function uses email and password for authentication, differing from the `oauth2` method which uses client credentials.

These functions facilitate secure and efficient communication with the Stoa API,
enabling the exchange of data through authenticated requests.

**Example usage**::

    from ds_stoa.authentication import oauth2, rest

    token = oauth2(
        client_id="your_client_id",
        client_secret="your_client_secret",
    )

    token = rest(
        email="your_email",
        password="your_password",
    )

"""

from ._oauth2 import oauth2
from ._rest import rest

__all__ = ["oauth2", "rest"]
