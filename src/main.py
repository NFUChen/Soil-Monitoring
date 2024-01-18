import sys

from loguru import logger

from messaging.message_broker import MessageBroker
from repository import (
    AlertConfigRepository, 
    EnvironmentVariableRepository,
    WaterReplenishmentConfigRepository
)
from service import (
    MonitorService, 
    WaterReplenishmentService, 
    OutputPin
)
from web.flask_server import FlaskServer

logger.remove()
logger.add(sys.stderr, level= "INFO")


message_broker = MessageBroker()
flask_server = FlaskServer(message_broker)

env_repo = EnvironmentVariableRepository()
alert_config_repo = AlertConfigRepository()
water_replenishment_config_repo = WaterReplenishmentConfigRepository()

monitor_service = MonitorService(env_repo, alert_config_repo, water_replenishment_config_repo,message_broker)

output_pin = OutputPin(17)
water_replenishment_service = WaterReplenishmentService(message_broker,water_replenishment_config_repo, output_pin)


@flask_server.app.route('/api/device/turn_on', methods=['GET'])
def turn_on():
    water_replenishment_service.turn_on()
    return "Success"

@flask_server.app.route('/api/device/turn_off', methods=['GET'])
def turn_off():
    water_replenishment_service.turn_off()
    return "Success"

if __name__ == "__main__":
    flask_server.run()