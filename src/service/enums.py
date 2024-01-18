from enum import Enum


class MessageTopic(Enum):
    REPLENISHMENT = "replenishment"
    SENSOR = "sensor"
    ALERT_HUMIDITY = "alert/humidity"
    ALERT_TEMPERATURE = "alert/temperature"

    MANUAL_REPLENISHMENT = "manual_replenishment"


class DeviceCommand(Enum):
    ON = "ON"
    OFF = "OFF"
