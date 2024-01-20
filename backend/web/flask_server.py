import time
from dataclasses import dataclass
from threading import Thread

from flask import Flask
from flask.views import MethodView
from flask_cors import CORS
from flask_socketio import SocketIO

from messaging.message_broker import IMeessageListener, MessageBroker
from repository.environment_variable_repository import EnvironmentVariable
from service.enums import MessageTopic
from web.server import Server


@dataclass
class SocketMessage:
    topic: str
    content: str

class FlaskServer(Server[MethodView]):
    ALL_HOSTS = "0.0.0.0"
    def __init__(self, message_broker: MessageBroker) -> None:
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app)
        CORS(self.app)

        self.message_broker = message_broker

        self.message_queue:list[SocketMessage] = []
        self._start_socket_message_handler_thread()
        self._subscribe()

    def _subscribe(self) -> None:
        topic_with_handlers: dict[str, IMeessageListener] = {
            MessageTopic.SENSOR.value: self._handle_sensor_emit,
            MessageTopic.ALERT_HUMIDITY.value: self._handle_alert_humidity,
            MessageTopic.ALERT_TEMPERATURE.value: self._handle_alert_temperature
        }

        for topic, handler in topic_with_handlers.items():
            self.message_broker.subscribe(topic, handler)
        
    def emit(self, topic: str, message: str) -> bool:
        self.socketio.emit(topic, message)

        return True

    def run(self) -> None:
        self.socketio.run(self.app, host= self.ALL_HOSTS, debug= False) # type: ignore

    def _handle_alert_humidity(self, topic, alert_message: str) -> None:
        self.message_queue.append(SocketMessage(topic, alert_message))

    def _handle_alert_temperature(self, topic, alert_message: str) -> None:
        self.message_queue.append(SocketMessage(topic, alert_message))

    def _handle_sensor_emit(self, topic: str, env_var: EnvironmentVariable) -> None:
        self.message_queue.append(SocketMessage(topic, str(env_var.to_dict())))

    def register_routes(self, request_mapping: str, method_view: MethodView) -> None:
        self.app.add_url_rule(request_mapping, view_func= method_view.as_view(request_mapping))

    def _start_socket_message_handler_thread(self) -> None:
        def wrapper() -> None:
            while (True):
                time.sleep(0.001)
                if len(self.message_queue) == 0:
                    continue
                
                socket_message = self.message_queue.pop(0)
                self.socketio.emit(socket_message.topic, socket_message.content)

        Thread(target= wrapper).start()


    
    
    