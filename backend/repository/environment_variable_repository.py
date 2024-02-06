
from abc import ABC, abstractmethod
from dataclasses import dataclass

from .externals import AHT20


@dataclass
class EnvironmentVariable:
    temperature: float
    humidity: float

    def to_dict(self) -> dict[str, float]:
        return self.__dict__

class EnvironmentVariableRepository(ABC):

    @abstractmethod
    def get_environment_variable(self) -> EnvironmentVariable:
        raise NotImplementedError()


class InMemoryEnvironmentVariableRepository(EnvironmentVariableRepository):
    def __init__(self) -> None:
        self.temperature = 28.2
        self.humidity = 24.3


    def get_environment_variable(self) -> EnvironmentVariable:
        return EnvironmentVariable(
            self.temperature,
            self.humidity
        )

class Aht20EnvironmentVariableRepository(EnvironmentVariableRepository):
    def __init__(self, aht20: AHT20) -> None:
        self.driver = aht20
    
    def get_environment_variable(self) -> EnvironmentVariable:
        return EnvironmentVariable(
            round(self.driver.get_temperature(), 2),
            round(self.driver.get_humidity(), 2)
        )