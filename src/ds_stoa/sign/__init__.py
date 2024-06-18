"""
This module facilitates the generation of pre-signed URLs
for secure data retrieval from the GraspDP datalake.

By leveraging the `sign` function, users can obtain URLs
that grant temporary access to specific files stored within the datalake.
This is particularly useful for scenarios where direct access to the data
is necessary without compromising security or requiring permanent credentials.

The `sign` function requires an authentication token and parameters
specifying the data to be accessed. It communicates with the Stoa service
to generate a URL that is pre-signed with the necessary permissions.

**Example Usage**::

    from ds_stoa.sign import sign

    # Authentication token and parameters for the request
    token = "your_auth_token"
    params = {"key": "12345"}

    # Generate a pre-signed URL
    pre_signed_url = sign(token=token, params=params)
    print(pre_signed_url)
"""

from ._sign import sign

__all__ = ["sign"]
