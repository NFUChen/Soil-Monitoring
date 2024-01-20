from flask.views import MethodView
from messaging.message_broker import MessageBroker
from repository.alert_config_repository import AlertConfigRepository
from repository.water_replenishment_config_repository import WaterReplenishmentConfigRepository
from service.water_replenishment_service.water_replenishment_service import WaterReplenishmentService
from web.server import Server
from web.flask_server import FlaskServer


def create_app(
    broker: MessageBroker, 
    water_replenishment_service: WaterReplenishmentService, 
    water_replenishment_config_repo: WaterReplenishmentConfigRepository,
    alert_config_repo: AlertConfigRepository) -> Server[MethodView]:
    server = FlaskServer(broker)
    
    
    @server.app.route('/api/device/turn_on', methods=['GET'])
    def turn_on():
        water_replenishment_service.turn_on()
        return "Success"

    @server.app.route('/api/device/turn_off', methods=['GET'])
    def turn_off():
        water_replenishment_service.turn_off()
        return "Success"

    @server.app.route("/api/config/water_replenishment", methods= ["GET"])
    def get_water_replenishment_config():
        return water_replenishment_config_repo.config.serialize()

    @server.app.route("/api/config/alert", methods= ["GET"])
    def get_alert_config():
        return alert_config_repo.config.serialize()
    
    
    
    
    return server
    