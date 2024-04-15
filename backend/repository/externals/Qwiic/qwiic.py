
import time
import qwiic_soil_moisture_sensor



class Qwiic:
    def __init__(self) -> None:
        self.qwiic_soil_moisture_sensor = qwiic_soil_moisture_sensor.QwiicSoilMoistureSensor()


        self._init_sensor()
       
    def _init_sensor(self) -> None:
        if self.qwiic_soil_moisture_sensor.connected == False:
            raise ValueError("The Qwiic Soil Moisture Sensor device isn't connected to the system. Please check your connection")
        
        self.qwiic_soil_moisture_sensor.begin()

        while True:
            time.sleep(1)
            self.qwiic_soil_moisture_sensor.read_moisture_level()
    

    def get_moisture_level(self) -> int:
        return self.qwiic_soil_moisture_sensor.level
            
        