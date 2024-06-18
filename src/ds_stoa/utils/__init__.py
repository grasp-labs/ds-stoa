"""
This module initializes the utility package for the Stoa project.
It makes the logger and exceptions modules available for import
when the utility package is imported elsewhere in the project.

The logger module provides logging functionality to track events
and errors during the execution of the program. The exceptions module
defines custom exceptions specific to the Stoa project,
allowing for more precise error handling.

**Example usage**::

    from utils.logger import LOGGER
    LOGGER.info("Logging information")
"""

from . import logger, exceptions

__all__ = ["logger", "exceptions"]
