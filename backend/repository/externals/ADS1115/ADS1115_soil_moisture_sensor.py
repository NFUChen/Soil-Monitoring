from typing import Optional
from loguru import logger
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


class ADS1115SoilMoistureSensor:
    def __init__(self) -> None:
        # Create the I2C bus
        i2c = busio.I2C(board.SCL, board.SDA)
        # Create the ADS object
        self.ads = ADS.ADS1115(i2c)
        # Set the gain
        self.ads.gain = 1
        # Create a single-ended input on channel 0
        self.chan = AnalogIn(self.ads, ADS.P0)
        # Define the sensor dry and wet values (adjust these as per calibration)
        self.dry_value = 20000  # Typical value for dry soil
        self.wet_value = 10000  # Typical value for wet soil

    def get_moisture_level(self) -> Optional[float]:
        try:
            # Read the value from the sensor
            soil_moisture_value = self.chan.value
            # Map the sensor value to a percentage (0-100)
            if soil_moisture_value > self.dry_value:
                soil_moisture_percentage = 0
            elif soil_moisture_value < self.wet_value:
                soil_moisture_percentage = 100
            else:
                soil_moisture_percentage = (
                    (self.dry_value - soil_moisture_value)
                    * 100
                    / (self.dry_value - self.wet_value)
                )
            # Constrain the percentage to be within 0 to 100
            soil_moisture_percentage = max(0, min(soil_moisture_percentage, 100))
            return soil_moisture_percentage
        except Exception as e:
            logger.critical(f"Error reading soil moisture: {e}")
            return
