

import time
from threading import Thread

from loguru import logger

from messaging.message_broker import MessageBroker
from repository.alert_config_repository import AlertConfigRepository
from repository.environment_variable_repository import (
    EnvironmentVariable, EnvironmentVariableRepository)
from repository.water_replenishment_config_repository import \
    WaterReplenishmentConfigRepository
from service.enums import MessageTopic


class MonitorService:
    ONE_DAY_SECONDS =  3600 * 24
    def __init__(self, 
                 environment_variable_repo: EnvironmentVariableRepository, 
                 alert_config_repo: AlertConfigRepository, 
                 water_replenishment_config_repo: WaterReplenishmentConfigRepository,
                 message_broker: MessageBroker) -> None:
        self.message_broker = message_broker
        self.alert_config_repo = alert_config_repo
        self.environment_variable_repo = environment_variable_repo
        self.water_replenishment_config_repo = water_replenishment_config_repo


        self._start_monitor_thread()

    

    def _handle_replenishment(self, second_in_day: int) -> None:
        is_reset_time = second_in_day > self.ONE_DAY_SECONDS - 5

        for replenishment in self.water_replenishment_config_repo.get_config().replenishment_times:
            if is_reset_time:
                if not replenishment.is_done:
                    continue
                replenishment.is_done = False

            if replenishment.is_done or is_reset_time:
                continue


            if second_in_day < replenishment.timestamp:
                continue
            
            self.message_broker.publish(MessageTopic.REPLENISHMENT.value, replenishment)
            replenishment.is_done = True



    def get_environment_variable(self) -> EnvironmentVariable:
        return self.environment_variable_repo.get_environment_variable()
    
    def _start_monitor_thread(self) -> None:
        def wrapper() -> None:
            
            while (True):
                current_epoch_seconds = int(time.time()) + (3600 * 8)
                second_in_day = self._get_second_in_day_from_epoch(current_epoch_seconds)

                alert_config = self.alert_config_repo.get_config()
                
                env_var = self.environment_variable_repo.get_environment_variable()
                env_var_passing = self.environment_variable_repo.get_environment_variable()
                
                if not (alert_config.humidity_threshold.lower_bound < env_var.humidity < alert_config.humidity_threshold.upper_bound):
                    humidity_alert_message = f"Humidity: {env_var.humidity} out of bound [{alert_config.humidity_threshold.lower_bound}, {alert_config.humidity_threshold.upper_bound}]"

                    self.message_broker.publish(MessageTopic.ALERT.value, humidity_alert_message)
                    self.message_broker.publish(MessageTopic.ALERT_HUMIDITY.value, humidity_alert_message)
                
                if not (alert_config.temperature_threshold.lower_bound < env_var.temperature < alert_config.temperature_threshold.upper_bound):
                    temperature_alert_message = f"Temperature: {env_var.temperature} out of bound [{alert_config.temperature_threshold.lower_bound}, {alert_config.temperature_threshold.upper_bound}]"
                    
                    self.message_broker.publish(MessageTopic.ALERT.value, temperature_alert_message)
                    self.message_broker.publish(MessageTopic.ALERT_TEMPERATURE.value, temperature_alert_message)

                
                self.message_broker.publish(MessageTopic.SENSOR.value, env_var_passing)
                

                if (current_epoch_seconds % 10) == 0:
                    self.environment_variable_repo.save(env_var)


                self._handle_replenishment(second_in_day)

                time.sleep(1)

                
        Thread(target = wrapper, daemon= True).start()
    
    def _get_second_in_day_from_epoch(self, current_epoch_seconds: int) -> int:
        return current_epoch_seconds % self.ONE_DAY_SECONDS