
import json
from dataclasses import dataclass
from typing import Any

from repository.serializable import Serializable


@dataclass
class GmailNotificationConfig(Serializable):
    email_sender: str
    password: str
    
    
class GmailNotificationConfigRepository:
    def __init__(self) -> None:
        self._config_file_name = "/app/repository/configs/.gmail-notification-config.json"
        self.config = self._read_config()
        

    def _read_config(self) -> GmailNotificationConfig:
        
        with open(self._config_file_name) as file:
            py_dict = json.loads(file.read())
            config = GmailNotificationConfig(**py_dict)
            return config
        
    def save_config(self, config:GmailNotificationConfig) -> dict[str, Any]:
         with open(self._config_file_name) as file:
            py_dict = config.serialize()
            file.write(json.dumps(py_dict, indent= False))
            return py_dict
        
    
    def get_config(self) -> GmailNotificationConfig:
        return self.config
    