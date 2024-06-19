# Grasp Labs AS - Stoa Package

## Overview

The `Stoa` package, developed by Grasp Labs AS, is a core component of our communication and data exchange system. The `Stoa` class offers essential functionalities for fetching, signing, authenticating, and ordering messages. These operations are fundamental for ensuring the integrity, authenticity, and proper sequencing of messages within our system.

## Installation

You can install the `Stoa` package via pip:

```bash
pip install ds-stoa
```

## Usage

Below are examples demonstrating how to utilize the `Stoa` class to handle message operations:

### Initialization

Initialize the `Stoa` class with required parameters:


```python
from stoa import Stoa

stoa = Stoa(
    authentication="oauth2",
    product_group_name="group1",
    product_name="product1",
    workspace="apps",
    owner_id="owner123",
    client_id="your_client_id",
    client_secret="your_client_secret",
)
```

### Authentication

Authenticate using the specified method:

```python
stoa.authenticate()

assert stoa.is_authenticated():
```

### Ordering

Create simple orders to be pre-signed.

```python
order_ids = stoa.order()
print(f"Ordered IDs: {order_ids}")
```


### Signing

Sign order to ensure their integrity and authenticity:

```python
signatures = stoa.sign()
print(f"Signatures: {signatures}")
```

### Fetch

Fetch method automatically handles the order and sign.

    - Authenticate
    - Order
    - Sign
    - Fetch

One can decide output format (default pd.Dataframe).
```python
# Fetch as JSON
fetched_data_json = stoa.fetch(format="json")
print(f"Fetched Data (JSON): {fetched_data_json}")

# Fetch as DataFrame
fetched_data_df = stoa.fetch(format="dataframe")
print(f"Fetched Data (DataFrame):\n{fetched_data_df}")
```


## Class Details

### Stoa Class

The `Stoa` class provides methods for handling messages within our system, including operations for fetching, signing, authenticating, and ordering messages.

#### Constructor

```python
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
) -> None
```

#### Parameters:

* authentication (str): The authentication method to use ("rest" or "oauth2").
* product_group_name (str): The name of the product group.
* product_name (str): The name of the product.
* workspace (str): The workspace where the product is located ("apps" or "cart").
* owner_id (str): The ID of the product owner.
* version (str): The version of the product (default: "1.0").
* offset (int): The offset for pagination (default: 0).
* limit (int): The limit for pagination (default: 20).
* ascending (bool): Whether to sort in ascending order (default: False).
* email (Optional[str]): The email for REST authentication (default: None).
* password (Optional[str]): The password for REST authentication (default: None).
* client_id (Optional[str]): The client ID for OAuth2 authentication (default: None).
* client_secret (Optional[str]): The client secret for OAuth2 authentication (default: None).

#### Methods

* authenticate() -> None: Authenticates a message to verify its origin.
* is_authenticated() -> bool: Checks if a message is authenticated.
* order() -> List[str]: Orders messages based on predefined rules.
* sign() -> Dict: Signs messages to ensure their integrity and authenticity.
* fetch(format: Literal["json", "dataframe"]) -> Union[List[Dict], pd.DataFrame]: Fetches messages in the specified form


## License

This package is licensed under the MIT License.


## Contact
For further information or assistance, please contact `Grasp Labs AS` support at hello@grasplabs.com.
