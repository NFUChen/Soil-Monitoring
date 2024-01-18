

import time
from dataclasses import dataclass
from typing import Any


@dataclass
class WaterReplenishment:
    timestamp: int
    duration: float
    target: str
    is_done: bool = False
    def to_dict(self) -> dict[str, Any]:
        return self.__dict__
    


@dataclass
class WaterReplenishmentConfig:
    replenishment_times: list[WaterReplenishment]

    def to_dict(self) -> dict[str, Any]:
        return {
            "replenishment_times": [replenish.to_dict() for replenish in self.replenishment_times]
        }

class WaterReplenishmentConfigRepository:
    def __init__(self) -> None:
       # Get the current time
        current_time = int(time.time()) % (3600 * 24)

        self.config = WaterReplenishmentConfig([
        WaterReplenishment(current_time + 10, 3, "1"),
        WaterReplenishment(current_time + 20, 5, "2"),
        WaterReplenishment(current_time + 30, 8, "3"),
    ])

    def get_config(self) -> WaterReplenishmentConfig:
        return self.config