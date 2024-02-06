import os
import sys

from loguru import logger

from messaging.message_broker import MessageBroker
from repository import (
    AlertConfigRepository, 
    EnvironmentVariableRepository, 
    WaterReplenishmentConfigRepository,
    InMemoryEnvironmentVariableRepository
)
from service import MonitorService, OutputPin, WaterReplenishmentService
from web.create_flask_app import create_app
logger.remove()
logger.add(sys.stderr, level= "INFO")


message_broker = MessageBroker()

env_repo: EnvironmentVariableRepository = InMemoryEnvironmentVariableRepository()

if os.environ["MODE"] == "PROD":
    logger.info("[PROD MODE DETECTED] Current mode is production mode, use AHT20 powered environment repository.")
    from repository import AHT20, Aht20EnvironmentVariableRepository
    aht20 = AHT20()
    env_repo = Aht20EnvironmentVariableRepository(aht20)

    


alert_config_repo = AlertConfigRepository()
water_replenishment_config_repo = WaterReplenishmentConfigRepository()

monitor_service = MonitorService(env_repo, alert_config_repo, water_replenishment_config_repo,message_broker)

output_pin = OutputPin(17)
water_replenishment_service = WaterReplenishmentService(message_broker,water_replenishment_config_repo, output_pin)

server = create_app(message_broker, water_replenishment_service, water_replenishment_config_repo, alert_config_repo)



if __name__ == "__main__":
    server.run()