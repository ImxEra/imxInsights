from dataclasses import dataclass


@dataclass
class ImxRailConnection:
    track: any
    passages: list[any]
