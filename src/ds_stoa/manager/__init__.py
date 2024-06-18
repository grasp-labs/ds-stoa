"""
Manager module for the Stoa class.

This module serves as the manager for the Stoa class, facilitating the management
of messages within our system. The Stoa class provides methods for fetching, signing,
authenticating, and ordering messages, which are crucial for secure and efficient
communication and data exchange.

**Usage Examples**:

1. Creating an instance of the Stoa class with REST authentication::

    from ds_stoa.manager.client import StoaClient

    stoa = StoaClient(
        authentication="rest",
        product_group_name="exampleGroup",
        product_name="exampleProduct",
        workspace="apps",
        owner_id="owner123",
        email="user@example.com",
        password="securepassword"
    )

    stoa.authenticate()
    assert stoa.is_authenticated()


2. Creating an instance of the Stoa class with OAuth2 authentication::

    from ds_stoa.manager.client import StoaClient

    stoa = StoaClient(
        authentication="oauth2",
        product_group_name="exampleGroup",
        product_name="exampleProduct",
        workspace="cart",
        owner_id="owner456",
        client_id="client_id_example",
        client_secret="client_secret_example"
    )

    stoa.authenticate()
    assert stoa.is_authenticated()


3. Order, Sign & Fetch::

    stoa = StoaClient(**params)
    order_ids = stoa.order()
    signatures = stoa.sign()
    dataframe = stoa.fetch()


**Note**: Replace the placeholder values (e.g., "user@example.com", "securepassword", "client_id_example", etc.)
with your actual data when implementing these examples.
"""

from .client import StoaClient

__all__ = ["StoaClient"]
