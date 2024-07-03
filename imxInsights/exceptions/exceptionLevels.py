from enum import Enum


class ErrorLevelEnum(Enum):
    """Enumeration of error levels with corresponding descriptions."""

    SUCCESS = "SUCCESS"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
