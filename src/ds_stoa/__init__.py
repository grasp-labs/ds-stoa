"""
The `ds-stoa` package: Data Science Project Management Made Easy

`ds-stoa` is a comprehensive Python package designed to streamline the management of data science projects, with a particular focus on facilitating efficient datalake transfers within graspDP projects. This package offers a suite of tools and utilities engineered to simplify the complexities associated with data handling, ensuring data scientists can focus more on analysis and less on data management.

The package includes the following subpackages for a complete workflow:

- `authentication`: For handling authentication mechanisms with the datalake.
- `fetch`: To fetch or retrieve data files from the datalake once an order is signed.
- `manager`: Utilizes all other modules to provide a high-level interface for managing datalake transfers.
- `order`: For creating and managing orders for data from the datalake.
- `sign`: To sign and validate orders for data retrieval.
- `utils`: Provides utility functions and helpers that support the other modules.

**Features**:

- Easy-to-use interfaces for managing datalake transfers.
- Integration capabilities with graspDP projects for seamless data workflows.
- A modular design allowing for easy expansion and customization.

**Dependencies**:

- Requires Python 3.7 or later.
- Additional dependencies may be required for specific utilities within the package.

**Example Usage**::

    from ds_stoa.manager import StoaClient

    # Initialize the manager for a datalake transfer
    client = StoaClient(**params)
    dataframe = client.fetch()

For more detailed documentation, please refer to the individual module descriptions.
"""

from . import authentication
from . import fetch
from . import manager
from . import order
from . import sign


__all__ = [
    "authentication",
    "fetch",
    "manager",
    "order",
    "sign",
]
