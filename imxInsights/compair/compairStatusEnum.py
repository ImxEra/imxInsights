from enum import Enum


class CompairStatus(Enum):
    """Change Identifier Enum."""

    CREATED = "created"
    """Object or attribute is created"""

    DELETED = "deleted"
    """Object or attribute is deleted"""

    CHANGED = "changed"
    """Object or attribute is changed"""

    NOT_CHANGED = "not changed"
    """Object or attribute is not changed"""

    NOT_PRESENT = "not present"
    """Object or attribute is not present"""

    INITIAL_PRESENT = "initial present"
    """Object or attribute is initial present"""


def check_status_changed_deleted_or_created(
    status: list[CompairStatus],
) -> CompairStatus:
    """
    Determines the overall status from a list of CompairStatus values.

    This function checks the list of `CompairStatus` values and returns the overall status based on the following rules:

    -   If all items in the list are `CompairStatus.NOT_PRESENT`, it returns `CompairStatus.NOT_PRESENT`.
    -   If any item in the list is `CompairStatus.CHANGED`, `CompairStatus.DELETED`, or `CompairStatus.CREATED`, it returns `CompairStatus.CHANGED`.
    -   Otherwise, it returns `CompairStatus.NOT_CHANGED`.

    Args:
        status: A list of `CompairStatus` values to evaluate.

    Returns:
        CompairStatus: The overall status based on the given list.
    """
    if all(item == CompairStatus.NOT_PRESENT for item in status):
        return CompairStatus.NOT_PRESENT
    elif any(
        element in [CompairStatus.CHANGED, CompairStatus.DELETED, CompairStatus.CREATED]
        for element in status
    ):
        return CompairStatus.CHANGED
    return CompairStatus.NOT_CHANGED
