import datetime
import re

from loguru import logger

from imxInsights.exceptions.customException import CustomException
from imxInsights.exceptions.exceptionLevels import ErrorLevelEnum
from imxInsights.imxContainer.tree.imxTreeObject import ImxObject


class ExceptionHandler:
    """Handler for logging and managing exceptions."""

    LOG_ROTATION_SIZE = "10 MB"

    def __init__(
        self, log_file: str, lvl: ErrorLevelEnum = ErrorLevelEnum.DEBUG
    ) -> None:
        """Initializes the ExceptionHandler.

        Args:
            log_file: The file where logs should be written.
            lvl: The default logging level.
        """
        self.log_file = log_file
        self.log_lvl: ErrorLevelEnum = lvl
        logger.add(log_file, rotation=self.LOG_ROTATION_SIZE, level=lvl.value)

    @staticmethod
    def handle_exception(
        exception: CustomException, return_log_as_str: bool = False
    ) -> str | None:
        """Handles a given exception by logging it and optionally raising it.

        Args:
            exception: The exception to be handled.
            return_log_as_str: Whether to return the log message as a string.

        Returns:
            The log message if return_log_as_str is True, otherwise None.

        Raises:
            The given exception if its level is CRITICAL.
        """
        log_level = exception.level.value

        log_msg = f"{exception.__class__.__name__}: {exception.msg}"

        if isinstance(exception.data, ImxObject):
            log_msg += f" - data: {exception.data.properties}"
        elif exception.data is not None:
            log_msg += f" - data: {exception.data}"

        logger.opt(depth=1).log(log_level, log_msg)

        if exception.level in [ErrorLevelEnum.CRITICAL]:
            raise exception

        if return_log_as_str:
            return f"{log_level} {log_msg}"

    @classmethod
    def create_new_log(cls, log_file: str, lvl: ErrorLevelEnum = ErrorLevelEnum.DEBUG):
        """Create a new log file.

        Args:
            log_file (str): The file where logs should be written.
            lvl (ErrorLevelEnum, optional): The default logging level. Defaults to ErrorLevelEnum.DEBUG.
        """
        logger.remove()
        logger.add(log_file, rotation=cls.LOG_ROTATION_SIZE, level=lvl.value)



# todo: we should have a seperated logger for every container, we cam use container id as a key...
timestamp = datetime.datetime.now().isoformat()
safe_timestamp = re.sub(r"[:]", "-", timestamp)
exception_handler = ExceptionHandler(f"imx_log_{safe_timestamp}.log")
