"""
Exception handling module.
"""

import json
from requests.exceptions import HTTPError


def enrich_http_exception(exc: HTTPError) -> None:
    """
    Enriches an HTTP exception with additional context without re-raising it.

    :param exc: Exception
    :return: None
    """
    try:
        content = exc.response.json()
    except json.JSONDecodeError:
        content = exc.response.text

    error = {
        "status_code": exc.response.status_code,
        "response": content,
        "exception": str(exc),
        "url": exc.request.url,
        "method": exc.request.method,
    }
    exc.args = (*exc.args, f"context: {json.dumps(error)}")
