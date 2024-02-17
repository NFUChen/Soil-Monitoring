import os
import sys

from loguru import logger

from messaging.message_broker import MessageBroker
from repository import (AlertConfigRepository, EmailReceiverRepository,
                        EnvironmentVariableRepository,
                        GmailNotificationConfigRepository,
                        InMemoryEnvironmentVariableRepository,
                        WaterReplenishmentConfigRepository, init_database)
from repository.models import EmailReceiver
from service import (CentralNotificationService, GmailNotificationService,
                     MonitorService, OutputPin, WaterReplenishmentService)
from web.create_flask_app import create_app

logger.remove()
logger.add(sys.stderr, level= "INFO") # type: ignore


message_broker = MessageBroker()
sql_engine = init_database()
env_repo: EnvironmentVariableRepository = InMemoryEnvironmentVariableRepository(sql_engine)

if os.environ.get("MODE", None) == "PROD":
    logger.info("[PROD MODE DETECTED] Current mode is production mode, use AHT20 powered environment repository.")
    from repository import AHT20, Aht20EnvironmentVariableRepository
    aht20 = AHT20()
    env_repo = Aht20EnvironmentVariableRepository(aht20, sql_engine)

    


alert_config_repo = AlertConfigRepository()
water_replenishment_config_repo = WaterReplenishmentConfigRepository()

monitor_service = MonitorService(env_repo, alert_config_repo, water_replenishment_config_repo,message_broker)

output_pin = OutputPin(17)
water_replenishment_service = WaterReplenishmentService(message_broker,water_replenishment_config_repo, output_pin)





email_receiver_repository = EmailReceiverRepository(sql_engine)
gmail_config_repo = GmailNotificationConfigRepository()
server = create_app(message_broker, water_replenishment_service, water_replenishment_config_repo, alert_config_repo, gmail_config_repo)


notification_services = [
    GmailNotificationService(1800, email_receiver_repository, gmail_config_repo)
    
]

central_notification_service = CentralNotificationService(
    message_broker, notification_services
)




if __name__ == "__main__":
    server.run()