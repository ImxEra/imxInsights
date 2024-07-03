from typing import Optional

from imxInsights.exceptions.exceptionLevels import ErrorLevelEnum


class CustomException(Exception):
    """Custom exception class.

    Attributes:
        msg: The exception message.
        level: The error level of the exception.
        data: Optional additional data associated with the exception.
    """

    def __init__(
        self,
        msg: str,
        level: ErrorLevelEnum = ErrorLevelEnum.ERROR,
        data: Optional[any] = None,
    ) -> None:
        """Initializes the CustomException.

        Args:
            msg: The exception message.
            level: The error level of the exception.
            data: Optional additional data associated with the exception.
        """
        super().__init__(msg)
        self.msg = msg
        self.level = level
        self.data = data
