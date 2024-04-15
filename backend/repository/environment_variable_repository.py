
import random
import time
from abc import ABC, abstractmethod
from threading import Thread
from typing import Iterable

from loguru import logger
from sqlalchemy import Engine
from sqlmodel import Session, select

from repository.models import EnvironmentVariable

from .externals.Qwiic import Qwiic
import Adafruit_DHT

class EnvironmentVariableDriver(ABC):
    @abstractmethod
    def get_environment_variable(self) -> EnvironmentVariable:
        raise NotImplementedError()
    

class DHT22WithQwiicEnvironmentVariableDriver(EnvironmentVariableDriver):
    def __init__(self) -> None:
        self.room_temperature_pin = 23
        self.driver = Adafruit_DHT

        self.qwiic_sensor = Qwiic()

        self.sensor = self.driver.DHT22
    
    def get_environment_variable(self) -> EnvironmentVariable:
        _, room_temperature = self.driver.read_retry(self.sensor, self.room_temperature_pin) # type: ignore
        soil_humidity = self.qwiic_sensor.get_moisture_level()

        if soil_humidity is None:
            humidity: float = 0
        if room_temperature is None:
            temperature: float = 0
        return EnvironmentVariable(
            temperature = round(humidity, 2),
            humidity = round(temperature, 2)
        )

class InMemoryEnvironmentVariableDriver(EnvironmentVariableDriver):
    def __init__(self) -> None:
        
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

class EnvironmentVariableRepository:
    ONE_DAY_SECONDS = (3600 *24)
    def __init__(self, driver: EnvironmentVariableDriver, sql_engine: Engine) -> None:
        self.driver = driver
        self.engine = sql_engine
    
    def get_environment_variable(self) -> EnvironmentVariable:
        return self.driver.get_environment_variable()
        
    def find_all_environment_variable_of_current_day(self, current_utc_epoch_time: int, hour_offset: int = 0) -> Iterable[EnvironmentVariable]:
        with Session(self.engine) as session:
            statement = select(EnvironmentVariable).where(
                ( EnvironmentVariable.timestamp or 0) // self.ONE_DAY_SECONDS == (current_utc_epoch_time + hour_offset * 3600) // self.ONE_DAY_SECONDS 
            )
            results = session.exec(statement)
            return results.all()
        
    
    def save(self, env_var: EnvironmentVariable) -> None:
        with Session(self.engine) as session:
            session.add(env_var)
            session.commit()