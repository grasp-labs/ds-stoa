"""DS-Stoa Logger."""

import logging
import sys
import tempfile
from typing import Optional

from ._context import ContextFilter, FolderNameFilter


class StoaLogger:
    """
    Setup logger for ds-stoa package.

    Usage:
    from ds_stoa.utils import LOGGER
    LOGGER.info("This is an info message.")
    LOGGER.warning("This is a warning message.")
    LOGGER.error("This is an error message.")
    LOGGER.debug("This is a debug message.")
    """

    LOGGER = logging.getLogger("STOA")
    FORMATER = logging.Formatter(
        "[%(asctime)s][%(name)s][%(levelname)s][%(folder_name)s]"
        "[%(funcName)s]: %(message)s",
        "%Y-%m-%d %H:%M:%S",
    )

    def __init__(self, log_level=logging.DEBUG) -> None:
        """
        Initialize the logger.

        :param log_level: The level of the logger.
        """
        self.LOGGER.setLevel(log_level)
        self.LOGGER.addHandler(self._setup_stream_handler())
        self._logger_file = None

    def setup_logger(self, prefix: str, with_file: bool = True) -> None:
        """
        Instantiates logger with a handler and a log message prefix.

        :param prefix: Prefix in log message.
        :param with_file: Indicates if logger should also write to file.
        :return: None
        """
        # to avoid multithread access, clear the handler when setup
        self.shutdown()
        self.LOGGER.addHandler(self._setup_stream_handler(prefix))
        if with_file:
            log_file = tempfile.NamedTemporaryFile(delete=False).name
            self.LOGGER.addHandler(self._setup_file_handler(log_file, prefix))

    def info(self, msg: str) -> None:
        """
        Log an info level message.

        :param msg: The message to log.
        :return: None
        """
        self.LOGGER.info(msg)

    def warning(self, msg: str) -> None:
        """
        Log a warning level message.

        :param msg: The message to log.
        :return: None
        """
        self.LOGGER.warning(msg)

    def error(self, msg: str) -> None:
        """
        Log an error level message.

        :param msg: The message to log.
        :return: None
        """
        self.LOGGER.error(msg)

    def debug(self, msg: str) -> None:
        """
        Log a debug level message.

        :param msg: The message to log.
        :return: None
        """
        self.LOGGER.debug(msg)

    @staticmethod
    def shutdown() -> None:
        """
        Shutdown the logger by removing all handlers.
        :return: None
        """
        StoaLogger.LOGGER.handlers = []

    def _setup_file_handler(
        self,
        log_file: str,
        prefix: str,
    ) -> logging.FileHandler:
        """
        Set up file handler for logger with logging prefix.

        :param log_file: The file to log to.
        :param prefix: The prefix for the log messages.
        :return: The file handler.
        """
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(self.FORMATER)
        file_handler.addFilter(ContextFilter(prefix))
        file_handler.name = "log-file"
        return file_handler

    def _setup_stream_handler(
        self,
        prefix: Optional[str] = None,
    ) -> logging.StreamHandler:
        """
        Sets up stream handler for logger with logging prefix.

        :param prefix: Prefix applied on every log to add context: Who!
        :return: The stream handler.
        """
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(self.FORMATER)
        stream_handler.addFilter(FolderNameFilter())
        stream_handler.addFilter(ContextFilter(prefix))
        stream_handler.name = "log-console"
        return stream_handler
