import RPi.GPIO as GPIO
import time

class security:
    def __init__(self):
        self.password = "password"
        GPIO.setwarnings(False) 
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def reset_pass(self, new_pass):
        self.password = new_pass

    def get_pass(self):
        return self.password


s = security()

while True:
    if GPIO.input(10) == GPIO.HIGH:
        print("Pressed")
        s.reset_pass("Root")
        print(s.get_pass())
        time.sleep(2)

