from enum import Enum


class CompairStatus(Enum):
    CREATED = "created"
    DELETED = "deleted"
    CHANGED = "changed"
    NOT_CHANGED = "not changed"
    NOT_PRESENT = "not present"
    INITIAL_PRESENT = "initial present"


def check_status_changed_deleted_or_created(
    status: list[CompairStatus],
) -> CompairStatus:
    if all(item == CompairStatus.NOT_PRESENT for item in status):
        return CompairStatus.NOT_PRESENT
    elif any(
        element in [CompairStatus.CHANGED, CompairStatus.DELETED, CompairStatus.CREATED]
        for element in status
    ):
        return CompairStatus.CHANGED
    return CompairStatus.NOT_CHANGED
