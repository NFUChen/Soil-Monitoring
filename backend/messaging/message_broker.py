import time
from dataclasses import dataclass
from threading import Thread
from typing import Any, Callable, Optional

from loguru import logger

from .mqtt_client import MqttClient


@dataclass
class Message:
    topic: str
    content: Any

IMeessageListener = Callable[[str, Any], None]

class MessageBroker:
    MESSAGE_SIZE = 1000
    def __init__(self, mqtt_client: Optional[MqttClient] = None) -> None:
        self.client = mqtt_client
        self.messages: list[Message] = []
        self.subscription: dict[str, list[IMeessageListener]]  = {}

        self._loop_start()

    def subscribe(self, topic: str, callback: IMeessageListener) -> None:
        if topic not in self.subscription:
            self.subscription[topic] = []
        self.subscription[topic].append(callback)
        logger.info(f"[TOPIC SUBSCRIPTION] Subscribing to topic: {topic}, callbacks: {[func.__name__ for func in self.subscription[topic]]}")
        if self.client is None:
            return

        self.client.subscribe(topic, callback)
    
    def publish(self, topic: str, content: Any) -> bool:
        if len(self.messages) > self.MESSAGE_SIZE:
            logger.warning(f"[MESSAGE SIZE EXCEEDED] Message size exceeded: {self.MESSAGE_SIZE}")
            return False
        logger.debug(f"[MESSAGE PUBLICATION] Message: {content} published to {topic}")
        message = Message(topic, content)
        self.messages.append(message)

        if self.client is None:
            return True
        
        self.client.publish(topic, content)
        return True
    
    def _loop_start(self) -> None:
        def wrapper() -> None:
            while (True):
                time.sleep(0.001)
                if len(self.messages) == 0:
                    continue
                broker_message = self.messages.pop(0)
                topic = broker_message.topic
                if topic not in self.subscription:
                    continue
                message_listeners = self.subscription.get(broker_message.topic, [])
                for message_listener in message_listeners:
                    func = lambda: message_listener(broker_message.topic, broker_message.content)
                    Thread(target= func, daemon= True).start()
                time.sleep(0.001)

        Thread(target = wrapper, daemon= True).start()



if __name__ == "__main__":
    message_broker = MessageBroker()
    def fox_callback(topic: str, content: str) -> None:
        print(f"[FOX] Received message on topic '{topic}': {content}")

    def dog_callback(topic: str, content: str) -> None:
        print(f"[DOG] Received message on topic '{topic}': {content}")

    message_broker.subscribe("news", fox_callback)
    # message_broker.subscribe("news", dog_callback)
    message_broker.publish("news", "New discovery in science!")
    while (True):
        message_broker.publish("news", "New discovery in science!")
        time.sleep(0.05)