"""
Module for Stoa API Authentication.
"""

from ._oauth2 import oauth2
from ._rest import rest

__all__ = ["oauth2", "rest"]
