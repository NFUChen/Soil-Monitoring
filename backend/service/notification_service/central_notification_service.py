from typing import Iterable

from loguru import logger

from messaging.message_broker import MessageBroker
from service.enums import MessageTopic
from service.notification_service.base_notification_service import \
    BaseNotificationService


class CentralNotificationService:
    def __init__(self, message_broker: MessageBroker ,notification_services: Iterable[BaseNotificationService]) -> None:
        self.notification_services = notification_services
        self.message_broker = message_broker

        self.message_broker.subscribe(MessageTopic.ALERT_HUMIDITY.value, self._subscribe_alert_notification_topic)
        self.message_broker.subscribe(MessageTopic.ALERT_TEMPERATURE.value, self._subscribe_alert_notification_topic)

    def _subscribe_alert_notification_topic(self, topic: str, message: str) -> None:
        logger.debug(f"[ALERT MESSAGE RECEIVING] Receive message from {topic} with message: {message}, begin pushing message to notification services...")
        for service in self.notification_services:
            service.push_notification(topic, message)
        
