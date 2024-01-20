
from dataclasses import dataclass


@dataclass
class EnvironmentVariable:
    temperature: float
    humidity: float

    def to_dict(self) -> dict[str, float]:
        return self.__dict__

class EnvironmentVariableRepository:
    def __init__(self) -> None:
        self.temperature = 28.2
        self.humidity = 24.3

        self._start_update_thread()


    def get_environment_variable(self) -> EnvironmentVariable:
        return EnvironmentVariable(
            self.temperature,
            self.humidity
        )
    
    def _start_update_thread(self) -> None:
         ...