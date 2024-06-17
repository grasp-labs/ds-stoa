"""
Authentication decorators.
"""

from functools import wraps
from typing import Callable, Any


def ensure_authenticated(method) -> Callable[..., Any]:
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        if not self.is_authenticated():
            self.authenticate()
        return method(self, *args, **kwargs)

    return wrapper
