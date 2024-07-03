from typing import Optional, Any

from imxInsights.exceptions.customException import CustomException
from imxInsights.exceptions.exceptionLevels import ErrorLevelEnum
from imxInsights.imxContainer.tree.imxTreeObject import ImxObject


class ImxException(CustomException):
    """IMX specific exception class."""

    def __init__(
        self,
        msg: str = "Generic Imx Exception",
        level: ErrorLevelEnum = ErrorLevelEnum.ERROR,
        data: Optional[Any] = None,
    ) -> None:
        """Initializes the ImxException.

        Args:
            msg: The exception message.
            level: The error level of the exception.
            data: Optional additional data associated with the exception.
        """
        super().__init__(msg, level, data)


class ImxUnconnectedExtension(ImxException):
    """Exception for unconnected IMX extension."""

    def __init__(
        self,
        msg: str = "Imx Exception object can not be matched to entity and is not connected",
        level: ErrorLevelEnum = ErrorLevelEnum.ERROR,
        data: Optional[ImxObject] = None,
    ) -> None:
        """Initializes the ImxUnconnectedExtension.

        Args:
            msg: The exception message.
            level: The error level of the exception.
            data: Optional additional data associated with the exception, expected to be an ImxObject.
        """
        super().__init__(msg, level, data)
        self.data: ImxObject = data


class ImxDuplicatedPuicsInContainer(ImxException):
    """Exception for duplicated PUICs in a container."""

    def __init__(
        self,
        msg: str = "Duplicated puic in container",
        level: ErrorLevelEnum = ErrorLevelEnum.CRITICAL,
        data: Optional[list[Any]] = None,
    ) -> None:
        """Initializes the ImxDuplicatedPuicsInContainer.

        Args:
            msg: The exception message.
            level: The error level of the exception.
            data: Optional additional data associated with the exception, expected to be a list.
        """
        super().__init__(msg, level, data)
        self.data: list[any] = data


class ImxRailConnectionRefNotPresent(ImxException):
    """Exception for building RailConnections where a PUICs is not present."""

    def __init__(
        self,
        msg: str = "puic not in container",
        level: ErrorLevelEnum = ErrorLevelEnum.ERROR,
        data: Optional[list[str]] = None,
    ) -> None:
        """Initializes the ImxRailConnectionRefNotPresent.

        Args:
            msg: The exception message.
            level: The error level of the exception.
            data: Optional additional data associated with the exception, expected to be a list.
        """
        super().__init__(msg, level, data)
        self.data: list[any] = data


class ImxTopologyExtensionNotPresent(ImxException):
    """Exception for building RailConnections where a PUICs is not present."""

    def __init__(
        self,
        msg: str = "puic not in container",
        level: ErrorLevelEnum = ErrorLevelEnum.ERROR,
        data: Optional[list[str]] = None,
    ) -> None:
        """Initializes the ImxRailConnectionRefNotPresent.

        Args:
            msg: The exception message.
            level: The error level of the exception.
            data: Optional additional data associated with the exception, expected to be a list.
        """
        super().__init__(msg, level, data)
        self.data: list[any] = data


class ImxRailConnectionMultiLinestring(ImxException):
    """Exception for building RailConnections where a PUICs is not present."""

    def __init__(
        self,
        msg: str = "puic not in container",
        level: ErrorLevelEnum = ErrorLevelEnum.ERROR,
        data: Optional[list[str]] = None,
    ) -> None:
        """Initializes the ImxRailConnectionRefNotPresent.

        Args:
            msg: The exception message.
            level: The error level of the exception.
            data: Optional additional data associated with the exception, expected to be a list.
        """
        super().__init__(msg, level, data)
        self.data: list[any] = data
