

from dataclasses import dataclass
from typing import Any


@dataclass
class Threshold:
    upper_bound: float
    lower_bound: float

    def to_dict(self) -> dict[str, float]:
        return self.__dict__
    


@dataclass
class AlertConfig:
    temperature_threshold: Threshold
    humimdity_threshold: Threshold

    def to_dict(self) -> dict[str, dict[str, float]]:
        return {
            "temperature_threshold": self.temperature_threshold.to_dict(),
            "humimdity_threshold": self.humimdity_threshold.to_dict()
        }

class AlertConfigRepository:
    def __init__(self) -> None:
        pass

    def get_config(self) -> AlertConfig:
        return AlertConfig(
            Threshold(24.3, 21.3),
            Threshold(44.3, 40.3)
        )
    
if __name__ == "__main__":
    # Example data
    temperature_threshold = Threshold(upper_bound=30.0, lower_bound=10.0)
    humidity_threshold = Threshold(upper_bound=80.0, lower_bound=20.0)

    alert_config = AlertConfig(
        temperature_threshold=temperature_threshold,
        humimdity_threshold=humidity_threshold
    )

    # Convert to dictionary
    example_data = alert_config.to_dict()

    print(example_data)