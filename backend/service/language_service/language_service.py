from enum import Enum


RESOURCES = {
    "en": {
        "temperature_out_of_bound": f"Temperature: {{current_temperature}} out of bound [{{lower_bound}}, {{upper_bound}}]",
        "humidity_out_of_bound": f"Humidity: {{current_humidity}} out of bound [{{lower_bound}}, {{upper_bound}}]"
    },
    "chi": {
        "temperature_out_of_bound": f"溫度: {{current_temperature}} 超出界線值 [{{lower_bound}}, {{upper_bound}}]",
        "humidity_out_of_bound": f"濕度: {{current_humidity}} 超出界線值 [{{lower_bound}}, {{upper_bound}}]"
    }
}

class TranslationKey(Enum):
    TMPERATURE_OUT_OF_BOUND = "temperature_out_of_bound"
    HUMIDITY_OUT_OF_BOUND = "humidity_out_of_bound"
class LanguageType(Enum):
    ENGLISH = "en"
    CHINESE = "chi"

class LanguageService:
    
    def __init__(self, language_resource: dict[str, dict[str, str]]) -> None:
        self.language_resource = language_resource
        self.language_type: LanguageType = LanguageType.CHINESE
    
    def change_language(self, language_type: LanguageType):
        self.language_type = language_type

    def translate(self, key: TranslationKey) -> str:
        language_content = self.language_resource[self.language_type.value]

        return language_content.get(key.value) or ""

