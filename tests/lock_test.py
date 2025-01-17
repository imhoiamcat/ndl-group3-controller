"""
This Raspberry Pi code was developed by newbiely.com
This Raspberry Pi code is made available for public use without any restriction
For comprehensive instructions and wiring diagrams, please visit:
https://newbiely.com/tutorials/raspberry-pi/raspberry-pi-electromagnetic-lock
"""


import RPi.GPIO as GPIO
import time

# Set the GPIO mode (BCM or BOARD)
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin controlled the electromagnetic lock via the relay module
RELAY_PIN = 12

# Set the relay pin as an output pin
GPIO.setup(RELAY_PIN, GPIO.OUT)

try:
    # Run the loop function indefinitely
    while True:
        # command = int(input("Enter the command.. "))
        # Turn the relay ON (HIGH) to lock the door
        GPIO.output(RELAY_PIN, GPIO.LOW)
        time.sleep(2)  # Wait for 2 seconds
        # Turn the relay OFF (LOW) to unlock the door
        GPIO.output(RELAY_PIN, GPIO.HIGH)
        time.sleep(2)  # Wait for 2 seconds

except KeyboardInterrupt:
    # If the user presses Ctrl+C, clean up the GPIO configuration
    GPIO.cleanup()
    
