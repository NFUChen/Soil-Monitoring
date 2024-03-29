
from __future__ import annotations

import json
import math
import time
from dataclasses import dataclass
from typing import Any, Optional

from loguru import logger

from .serializable import Serializable


@dataclass
class WaterReplenishment(Serializable):
    # make sure the time input is utc-based
    timestamp: int
    duration: float
    target: Optional[str] = None
    is_done: bool = False
    


@dataclass
class WaterReplenishmentConfig(Serializable):
    replenishment_times: list[WaterReplenishment]
    
    
    def __post_init__(self) -> None:
        replenishment_times:list[WaterReplenishment] = []
        for replenishment_time in self.replenishment_times:
            if isinstance(replenishment_time, dict):
                replenishment = WaterReplenishment(**replenishment_time)
                
                if isinstance(replenishment.timestamp, str):
                    replenishment.timestamp = self._time_string_to_seconds(replenishment.timestamp)
                replenishment_times.append(replenishment)
        if len(replenishment_times) == 0:
            return

        self.replenishment_times = replenishment_times

        self.replenishment_times = sorted(self._auto_merge_replenishments(), key= lambda replenishment: replenishment.timestamp)

    def _auto_merge_replenishments(self) -> list[WaterReplenishment]:
        logger.info("[REPLENISHMENT MERGING] Starting _auto_merge_replenishments function...")
        is_conflicting = False

        timestamp_set = set()
        for replenishment_time in self.replenishment_times:
            for timestamp in range(replenishment_time.timestamp, replenishment_time.timestamp + math.ceil(replenishment_time.duration)):
                if timestamp in timestamp_set:
                    is_conflicting = True
                timestamp_set.add(timestamp)

        
        if not is_conflicting:
            logger.info("[REPLENISHMENT MERGING ABORTING] No conflicting replenishments found.")
            return self.replenishment_times
        

        logger.info("[REPLENISHMENT MERGING REQUIRED] Conflicting replenishments found. Merging...")
        merged_replenishments: list[WaterReplenishment] = []
        for timestamp in timestamp_set:
            if (timestamp - 1) in timestamp_set: # searching for starting point
                continue
            logger.info(f"[REPLENISHMENT TIMESTAMP FOUND] Replenishment timestamp startigng porint found: {timestamp}")
            current_duration = 0
            while (timestamp + current_duration) in timestamp_set:
                logger.debug(f"[REPLENISHMENT DURATION INCREMENTING] Current duration: {current_duration}")
                current_duration += 1
            replenishment = WaterReplenishment(timestamp= timestamp, duration= current_duration)
            merged_replenishments.append(replenishment)
            logger.info(f"[ADD REPLENISHMENT] Replenishment appended: {replenishment}")

        logger.info("[REPLENISHMENT MERGING COMPLETE] Merging complete. Resulting replenishments:")
        for replenishment in merged_replenishments:
            logger.info(f"[REPLENISHMENT MERGING REPORT] Timestamp: {replenishment.timestamp}, Duration: {replenishment.duration}")
            
        return merged_replenishments
        
        
    def _time_string_to_seconds(self, time_str: str) -> int:
        # Split the time string into hours, minutes, and seconds
        hours, minutes, seconds = map(int, time_str.split(':'))

        # Calculate the total seconds
        total_seconds = hours * 3600 + minutes * 60 + seconds

        return total_seconds

class WaterReplenishmentConfigRepository:
    
    def __init__(self) -> None:

        self._config_file_name = "/app/repository/configs/.water-replenishment-config.json"
        self.config = self._read_config()
        

    def _read_config(self) -> WaterReplenishmentConfig:
        current_time = int(time.time()) % (3600 * 24)
        logger.info(f"[CONFIG READING TIME] Current second in day: {current_time}")
        with open(self._config_file_name) as file:
            py_dict = json.loads(file.read())
            config = WaterReplenishmentConfig(**py_dict)
            for replenishment_time in config.replenishment_times:
                replenishment_time.is_done = current_time > replenishment_time.timestamp

            logger.success(f"[REPLENISHMENT CONFIG READING] Reading config: {config}")
            return config
        
    
    def save_config(self, config:WaterReplenishmentConfig) -> dict[str, Any]:
        with open(self._config_file_name, "w") as file:
            py_dict = config.serialize()
            config_json = json.dumps(py_dict, indent= 4)
            file.write(config_json)
            
        self.config = config
        return py_dict
                

    def get_config(self) -> WaterReplenishmentConfig:
        return self.config
    