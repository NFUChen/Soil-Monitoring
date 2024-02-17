
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from .serializable import Serializable


@dataclass
class Threshold(Serializable):
    upper_bound: float
    lower_bound: float




@dataclass
class AlertConfig(Serializable):
    temperature_threshold: Threshold
    humidity_threshold: Threshold

    def __post_init__(self) -> None:
        if isinstance(self.temperature_threshold, dict):
            self.temperature_threshold = Threshold(**self.temperature_threshold)
            
        if isinstance(self.humidity_threshold, dict):
            self.humidity_threshold = Threshold(**self.humidity_threshold)
        


class AlertConfigRepository:
    def __init__(self) -> None:

        self._config_file_name = "/app/repository/configs/.alert-config.json"
        self.config = self._read_config()


    def _read_config(self) -> AlertConfig:
        with open(self._config_file_name) as file:
            py_dict = json.loads(file.read())
            return AlertConfig(**py_dict) # type: ignore
        
    def save_config(self, config: AlertConfig) -> dict[str, Any]:
        with open(self._config_file_name, "w") as file:
            py_dict = config.serialize()
            config_json = json.dumps(py_dict, indent= False)
            file.write(config_json)
        self.config = config
        return py_dict

    def get_config(self) -> AlertConfig:
        return self.config
    
if __name__ == "__main__":
    # Example data
    temperature_threshold = Threshold(upper_bound=30.0, lower_bound=10.0)
    humidity_threshold = Threshold(upper_bound=80.0, lower_bound=20.0)

    alert_config = AlertConfig(
        temperature_threshold=temperature_threshold,
        humidity_threshold=humidity_threshold
    )
    json_data = {'temperature_threshold': {'upper_bound': 30.0, 'lower_bound': 10.0}, 'humidity_threshold': {'upper_bound': 80.0, 'lower_bound': 20.0}}
    print(AlertConfig(**json_data)) # type: ignore
    print(alert_config.__dict__)
    
    print(temperature_threshold.serialize())
    print(alert_config.serialize())