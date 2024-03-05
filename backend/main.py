import os
import sys
from typing import Type

from loguru import logger

from messaging.message_broker import MessageBroker
from repository import (AlertConfigRepository, EmailReceiverRepository,
                        EnvironmentVariableRepository,
                        GmailNotificationConfigRepository,
                        WaterReplenishmentConfigRepository, init_database, 
                        AHT20EnvironmentVariableDriver, DHT20EnvironmentVariableDriver, InMemoryEnvironmentVariableDriver)
from repository.environment_variable_repository import EnvironmentVariableDriver
from repository.models import EmailReceiver
from service import (CentralNotificationService, GmailNotificationService,
                     MonitorService, OutputPin, WaterReplenishmentService,
                     RESOURCES, LanguageService)
from web.create_flask_app import create_app

logger.remove()
logger.add(sys.stderr, level= "INFO") # type: ignore


message_broker = MessageBroker()
sql_engine = init_database()

driver_lookup: dict[str, Type[EnvironmentVariableDriver]] = {
    "MEMORY": InMemoryEnvironmentVariableDriver,
    "AHT20": AHT20EnvironmentVariableDriver,
    "DHT20": DHT20EnvironmentVariableDriver
}

driver_key = os.environ.get("MODE", "MEMORY")

driver: EnvironmentVariableDriver = driver_lookup[driver_key]()


env_repo: EnvironmentVariableRepository = EnvironmentVariableRepository(driver, sql_engine)

language_service = LanguageService(RESOURCES)


alert_config_repo = AlertConfigRepository()
water_replenishment_config_repo = WaterReplenishmentConfigRepository()

monitor_service = MonitorService(env_repo, alert_config_repo, water_replenishment_config_repo,message_broker, language_service)

output_pin = OutputPin(17)
water_replenishment_service = WaterReplenishmentService(message_broker,water_replenishment_config_repo, output_pin)





email_receiver_repository = EmailReceiverRepository(sql_engine)
gmail_config_repo = GmailNotificationConfigRepository()
server = create_app(message_broker, water_replenishment_service, water_replenishment_config_repo, alert_config_repo, gmail_config_repo, env_repo, language_service)


notification_services = [
    GmailNotificationService(1800, email_receiver_repository, gmail_config_repo)
    
]

central_notification_service = CentralNotificationService(
    message_broker, notification_services
)




if __name__ == "__main__":
    server.run()