"""
Logger Module.

This module contains the logger for the DS-Stoa package.
"""

from ._logger import StoaLogger

StoaLogger = StoaLogger()
LOGGER = StoaLogger.LOGGER

__all__ = ["StoaLogger", "LOGGER"]
