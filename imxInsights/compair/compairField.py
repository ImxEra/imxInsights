from dataclasses import dataclass, field
from typing import Any

from imxInsights.compair.compairStatusEnum import (
    CompairStatus,
    check_status_changed_deleted_or_created,
)


@dataclass
class ImxFieldCompairValue:
    container_id: str
    value: Any
    status: CompairStatus = field(init=False)


class ImxFieldCompair:
    def __init__(self, name: str, values: list[tuple[str, Any]]):
        self.name: str = name
        self.values: list[ImxFieldCompairValue] = [
            ImxFieldCompairValue(item[0], item[1]) for item in values
        ]
        self.global_status: CompairStatus = CompairStatus.NOT_CHANGED
        self._set_status()
        self._set_global_status()

    def __repr__(self):
        return f"<ImxFieldCompair name={self.name} {[item.status.name for item in self.values]}/>"

    def _set_status(self):
        previous_value: Any = None

        for idx, item in enumerate(self.values):
            if idx == 0 and item.value is not None:
                item.status = CompairStatus.INITIAL_PRESENT
            elif previous_value is None and item.value is None:
                item.status = CompairStatus.NOT_PRESENT
            elif previous_value is None and item.value is not None:
                item.status = CompairStatus.CREATED
            elif previous_value is not None and item.value is None:
                item.status = CompairStatus.DELETED
            elif previous_value == item.value:
                item.status = CompairStatus.NOT_CHANGED
            elif previous_value != item.value and item.value is not None:
                item.status = CompairStatus.CHANGED

            previous_value = item.value

    def _set_global_status(self):
        self.global_status = check_status_changed_deleted_or_created(
            [item.status for item in self.values]
        )
