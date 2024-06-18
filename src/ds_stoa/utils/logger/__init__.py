"""
Logger Module.

This module contains the logger for the DS-Stoa package.
The logger is used to log events and errors during the execution of the program.
It provides a centralized location for logging, allowing for easy configuration
of log levels, formatting, and output destinations.
"""

from ._logger import StoaLogger

StoaLogger = StoaLogger()
LOGGER = StoaLogger.LOGGER

__all__ = ["StoaLogger", "LOGGER"]
