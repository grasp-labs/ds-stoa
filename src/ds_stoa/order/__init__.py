"""
This module provides functionality for interacting with the Stoa API
to place orders. It encapsulates the process of sending order requests
through the `order` function, which communicates with the Stoa API
to order products or services.

The `order` function is designed to be used by other parts of the
application that require interaction with the Stoa API for placing
orders. It simplifies the API interaction by abstracting the details
of the HTTP request and response handling.

**Example Usage**::

    from ds_stoa.order import order

    # Authentication token and parameters for the order
    token = "your_auth_token"
    params = {
        "product_group_name": "your_product_group_name",
        "product_name": "your_product_name",
        "workspace": "your_workspace",
        "owner_id": "your_owner_id",
        "version": "1.0",
        "offset": "0",
        "limit": "20",
        "ascending": "False",
    }

    # Send an order request
    order_ids = order(token=token, params=params)
    print(order_ids)
"""

from ._order import order

__all__ = ["order"]
