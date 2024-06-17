"""
Logger Context Filter

This module contains the context filter for the logger.
"""

import os
import logging
from typing import Literal, Optional


class ContextFilter(logging.Filter):
    """
    Context filter to add customized field in the logging
    record. This filter is used to add a prefix to the log.
    """

    def __init__(self, prefix: Optional[str] = None) -> None:
        """
        Constructor for the ContextFilter class.

        :param prefix: The prefix to add to the log record.
        :return: None
        """
        self._prefix = prefix

    def filter(self, record) -> Literal[True]:
        """
        Add prefix to the log record.

        :param record: The log record.
        :return: True
        """
        if not hasattr(record, "prefix"):
            record.prefix = "---"
        record.prefix = self._prefix
        return True


class FolderNameFilter(logging.Filter):
    def filter(self, record) -> Literal[True]:
        """
        Add the folder name to the log record.

        :param record: The log record.
        :return: True
        """
        folder_name = os.path.basename(os.path.dirname(record.pathname))
        record.folder_name = folder_name
        return True
