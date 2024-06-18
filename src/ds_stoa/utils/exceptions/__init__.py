"""
Module for handling exceptions.

This module provides a function to enrich HTTP exceptions with more context
such as the request URL, status code, and response body. This additional
context can be useful for debugging and logging errors that occur during
HTTP requests.
"""

from ._handler import enrich_http_exception

__all__ = ["enrich_http_exception"]
