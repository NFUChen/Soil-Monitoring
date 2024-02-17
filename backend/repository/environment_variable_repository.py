
import random
import time
from abc import ABC, abstractmethod
from threading import Thread

from loguru import logger
from sqlalchemy import Engine
from sqlmodel import Session

from repository.models import EnvironmentVariable

from .externals import AHT20


class EnvironmentVariableRepository(ABC):

    @abstractmethod
    def get_environment_variable(self) -> EnvironmentVariable:
        raise NotImplementedError()
    
    @abstractmethod
    def save(self, env_var: EnvironmentVariable) -> None:
        raise NotImplementedError()

class InMemoryEnvironmentVariableRepository(EnvironmentVariableRepository):
    def __init__(self, sql_engine: Engine) -> None:
        
        self.engine = sql_engine
        self.temperature = 28.2
        self.humidity = 24.3

        self.temperature_upper_bound = 31
        self.temperature_lower_bound = 28

        self.humidity_upper_bound = 80
        self.humidity_lower_bound = 48

        self._start_simulate_thread()


    def get_environment_variable(self) -> EnvironmentVariable:
        return EnvironmentVariable(
            temperature = round(self.temperature, 2),
            humidity = round(self.humidity, 2)
        )
    
    def _generate_random_float(self, minimum: int, maximum: int) -> float:
        """
        Generates a random float within the specified range [minimum, maximum].
        
        Args:
        minimum (float): The minimum value of the range (inclusive).
        maximum (float): The maximum value of the range (inclusive).
        
        Returns:
        float: A random float within the specified range.
        """
        return random.uniform(minimum, maximum)

    def _start_simulate_thread(self) -> None:
        logger.info("[IN MEMORY SIMULATION THREAD] Starting simulation thread for mocking temperature and humidity readings...")
        def wrapper() -> None:
            while (True):
                rand_float = self._generate_random_float(0, 1)
                self.temperature += rand_float
                self.humidity += rand_float

                if self.temperature > self.temperature_upper_bound:
                    self.temperature = self.temperature_lower_bound

                if self.humidity > self.humidity_upper_bound:
                    self.humidity = self.humidity_lower_bound
                time.sleep(1)

        Thread(target= wrapper).start()


    def save(self, env_var: EnvironmentVariable) -> None:
        with Session(self.engine) as session:
            session.add(env_var)
            session.commit()

class Aht20EnvironmentVariableRepository(EnvironmentVariableRepository):
    def __init__(self, aht20: AHT20, sql_engine: Engine) -> None:
        self.driver = aht20
        self.engine = sql_engine
    
    def get_environment_variable(self) -> EnvironmentVariable:
        return EnvironmentVariable(
            temperature = round(self.driver.get_temperature(), 2),
            humidity = round(self.driver.get_humidity(), 2)
        )
    
    def save(self, env_var: EnvironmentVariable) -> None:
        with Session(self.engine) as session:
            session.add(env_var)
            session.commit()