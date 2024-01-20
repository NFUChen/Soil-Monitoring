import time

from loguru import logger

from messaging.message_broker import MessageBroker
from repository import WaterReplenishment, WaterReplenishmentConfigRepository
from repository.water_replenishment_config_repository import \
    WaterReplenishmentConfig
from service.enums import DeviceCommand, MessageTopic
from service.hardware_device_service.output_pin import OutputPin


class WaterReplenishmentService:
    def __init__(self, 
                 message_broker: MessageBroker,
                 water_replenishment_config_repository: WaterReplenishmentConfigRepository, 
                 replenishment_output_device: OutputPin
        ) -> None:
        self.replenishment_output_device = replenishment_output_device
        self.water_replenishment_config_repository = water_replenishment_config_repository

        self.message_broker = message_broker
        
        self._subcribe()
        self._reset_device()
        
    
    def _reset_device(self) -> None:
        logger.warning("[INIT RESET] Turn off replenishment device")
        self.replenishment_output_device.force_turn_off()

    def _handle_auto(self, topic: str, replenishment: WaterReplenishment) -> None:
        logger.info(f"[AUTO REPLENISHMENT SIGNAL] Receiving replenishment signal from {topic} with replenishment: {replenishment}")
        logger.success("[REPLENISHMENT DEVICE CONTROL] Turn on replenishment device")
        self.replenishment_output_device.turn_on()
        time.sleep(replenishment.duration)
        logger.success("[REPLENISHMENT DEVICE CONTROL] Turn off replenishment device")
        self.replenishment_output_device.turn_off()

    def _handle_manual(self, topic: str, device_command: DeviceCommand) -> None:
        logger.info(f"[MANUAL REPLENISHMENT SIGNAL] Receiving replenishment command from {topic}: {device_command}")
        handler = {
            DeviceCommand.ON: self.replenishment_output_device.turn_on,
            DeviceCommand.OFF: self.replenishment_output_device.turn_off
        }[device_command]

        handler()

    def turn_on(self) -> None:
        self.replenishment_output_device.turn_on()

    def turn_off(self) -> None:
        self.replenishment_output_device.turn_off()



    def _subcribe(self) -> None:
        self.message_broker.subscribe(MessageTopic.REPLENISHMENT.value, self._handle_auto)
        self.message_broker.subscribe(MessageTopic.MANUAL_REPLENISHMENT.value, self._handle_manual)
        
    
    def get_config(self) -> WaterReplenishmentConfig:
        return self.water_replenishment_config_repository.get_config()

