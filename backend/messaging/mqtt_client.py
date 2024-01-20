import time
from threading import Thread
from typing import Callable

import paho.mqtt.client as mqtt
from loguru import logger

IMessageListener = Callable[[str, str], None]
 
class MqttClient:
    def __init__(self, broker_address: str, port: int = 1883):
        self.client: mqtt.Client = mqtt.Client()
        self.broker_address: str = broker_address
        self.port: int = port
 
        # Set callback functions
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
 
        self.subscription_map: dict[str, list[IMessageListener]] = {}
 
        self.is_checking_thread_start = False
 
    def subscribe(self, topic: str, callback: Callable) -> None:
        if not self.is_checking_thread_start:
            self._start_check_connection_thread()
 
 
        if topic not in self.subscription_map:
            self.subscription_map[topic] = []
 

        self.subscription_map[topic].append(callback)
    
    def _init_subscription(self) -> None:
        logger.info("[MQTT INIT SUBSCRIPTION] Initializing subscription map...")
        for topic in self.subscription_map:
            logger.info(f"[MQTT INIT SUBSCRIPTION] Subscribe to {topic}...")
            self.client.subscribe(topic, qos= 2)
 
    def on_connect(
        self, client: mqtt.Client, userdata: None, flags: dict, rc: int
    ) -> None:
        if rc == 0:
            logger.info("[MQTT CLIENT ON CONNECT] Connected to MQTT Broker")
            # Subscribe to the desired topic
            self._init_subscription()
        else:
            logger.info(f"[MQTT CLIENT ON CONNECT] Connection failed with code {rc}")
 
    def on_message(self, client: mqtt.Client, userdata: None, msg: mqtt.MQTTMessage) -> None:
        # This function will be called when a message is received
        topic = msg.topic
        if topic in self.subscription_map.keys():
            callbacks = self.subscription_map[topic]
            for callback in callbacks:
                callback(topic, msg.payload.decode())
 
    def connect(self) -> None:
 
        # Connect to the MQTT broker
        self.client.connect(self.broker_address, port=self.port, keepalive=60)
 
        # Start the MQTT loop
        self.client.loop_start()
 
    def disconnect(self) -> None:
        # Disconnect from the MQTT broker
        self.client.disconnect()
        self.client.loop_stop()
 
    def publish(self, topic: str, message: str) -> bool:
        if not self.client.is_connected:
            logger.info("[MQTT PUBLICATION UNSUCCESSFULLY] MQTT client is not connected, trying to reconnect...")
            self.client.reconnect()
            return False
        logger.info(f"[MQTT PUBLICATION SUCCESSFULLY] Publish {message} to {topic}")
        self.client.publish(topic, message, qos= 2)
        return True
 
    def _start_check_connection_thread(self):
        
        def wrapper():
            while (True):
                if (not self.client.is_connected()):
                    logger.critical(f"[MQTT CLIENT DISCONNECTION] Unable to connect with broker: {self.broker_address}, trying to reconnect.")
                    self.connect()
                    self._init_subscription()
                time.sleep(1)
        logger.info("[MQTT CONNECTION CHECKING THREAD START] Start MQTT client connection checking thread...")
        thread = Thread(target= wrapper)
        thread.start()
        self.is_checking_thread_start = True