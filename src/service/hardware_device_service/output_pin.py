import RPi.GPIO as GPIO
from loguru import logger

class OutputPin:
    def __init__(self, output_pin_number: int) -> None:
        self.output_pin_number = output_pin_number
        GPIO.setmode(GPIO.BCM) # type: ignore
        GPIO.setup(self.output_pin_number, GPIO.OUT, initial=GPIO.HIGH) # type: ignore
        self.is_turn_on = False

    def __del__(self) -> None:
        GPIO.cleanup(self.output_pin_number) # type: ignore

    def turn_on(self) -> bool:
        if self.is_turn_on:
            logger.warning(f"[POTENTIAL GPIO DEVICE CONTROL CONFLICT] Output pin: {self.output_pin_number} is already turned on, aborted")
            return False
        GPIO.output(self.output_pin_number, GPIO.LOW) # type: ignore
        self.is_turn_on = True
        logger.info(f"[GPIO DEVICE CONTROL] Turn on output pin: {self.output_pin_number}")
        return True
    
    def force_turn_off(self) -> bool:
        GPIO.output(self.output_pin_number, GPIO.HIGH) # type: ignore
        return True
    
    def turn_off(self) -> bool:
        if not self.is_turn_on:
            logger.warning(f"[POTENTIAL GPIO DEVICE CONTROL CONFLICT] Output pin: {self.output_pin_number} is already turned off, aborted")
            return False
        
        GPIO.output(self.output_pin_number, GPIO.HIGH) # type: ignore
        self.is_turn_on = False
        logger.info(f"[GPIO DEVICE CONTROL] Turn off output pin: {self.output_pin_number}")
        return True
