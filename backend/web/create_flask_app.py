import json
import time
from typing import Any

from flask import request
from flask.views import MethodView

from messaging.message_broker import MessageBroker
from repository.alert_config_repository import (AlertConfig,
                                                AlertConfigRepository)
from repository.environment_variable_repository import EnvironmentVariableRepository
from repository.gmail_notification_config_repository import (
    GmailNotificationConfig, GmailNotificationConfigRepository)
from repository.water_replenishment_config_repository import (
    WaterReplenishmentConfig, WaterReplenishmentConfigRepository)
from service.language_service.language_service import LanguageService, LanguageType
from service.water_replenishment_service.water_replenishment_service import \
    WaterReplenishmentService
from web.flask_server import FlaskServer
from web.server import Server


def create_app(
    broker: MessageBroker, 
    water_replenishment_service: WaterReplenishmentService, 
    water_replenishment_config_repo: WaterReplenishmentConfigRepository,
    alert_config_repo: AlertConfigRepository, 
    gmail_config_repo: GmailNotificationConfigRepository, 
    environment_variable_repo: EnvironmentVariableRepository,
    language_service: LanguageService) -> Server[MethodView]:
    server = FlaskServer(broker)
    
    
    @server.app.route('/api/device/turn_on', methods=['GET'])
    def turn_on() -> str:
        water_replenishment_service.turn_on()
        return "Success"

    @server.app.route('/api/device/turn_off', methods=['GET'])
    def turn_off() -> str:
        water_replenishment_service.turn_off()
        return "Success"
    
    @server.app.route("/api/device/is_turn_on", methods= ["GET"])
    def is_turn_on() -> dict[str, bool]:
        return {"is_turn_on": water_replenishment_service.is_turn_on()}

    @server.app.route("/api/config/water_replenishment", methods= ["GET"])
    def get_water_replenishment_config() -> dict[str, Any]:
        return water_replenishment_config_repo.config.serialize()

    @server.app.route("/api/config/alert", methods= ["GET"])
    def get_alert_config() -> dict[str, Any]:
        return alert_config_repo.config.serialize()
    
    @server.app.route("/api/config/water_replenishment", methods= ["POST"])
    def save_water_replenishment_config() -> dict[str, Any]:
        replenishment_dict:dict[str, Any] = request.get_json() # type: ignore
        return water_replenishment_config_repo.save_config(WaterReplenishmentConfig(**replenishment_dict))
    
    
    @server.app.route("/api/config/alert", methods= ["POST"])
    def save_water_alert_config() -> dict[str, Any]:
        alert_config_dict:dict[str, Any] = request.get_json() # type: ignore
        return alert_config_repo.save_config(AlertConfig(**alert_config_dict))
    
    @server.app.route("/api/config/gmail_notification", methods= ["POST"])
    def save_gmail_notification_config() -> dict[str, Any]:
        gmail_config_dict:dict[str, Any] = request.get_json() # type: ignore
        return gmail_config_repo.save_config(GmailNotificationConfig(**gmail_config_dict))
    
    @server.app.route("/api/report/daily_environment_variable", methods = ["GET"])
    def get_daily_environment_variables() -> dict[str, list[dict[str, Any]]]:
        return {
            "data": [
            env_var.to_dict() for env_var in environment_variable_repo.find_all_environment_variable_of_current_day(int(time.time()))
        ]
        }
    
    @server.app.route("/api/language/change_language", methods= ["POST"])
    def change_language() -> tuple[str, int]:
        language_dict: dict[str, str] = request.get_json() # type: ignore

        valid_language_types = [_type.name for _type in LanguageType]
        chosen_language = language_dict["language"]
        if chosen_language not in valid_language_types:
            return f"Unsupported language, please enter one of the following: {valid_language_types}", 400

        language_service.change_language(LanguageType[language_dict["language"]])

        return "Success", 200
        
    
    
        
    
    return server
    