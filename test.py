import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)


# Define the GPIO pin controlled the electromagnetic lock via the relay module
RELAY_PIN = 12

# Set the relay pin as an output pin
GPIO.setup(RELAY_PIN, GPIO.OUT)

GPIO.output(RELAY_PIN, GPIO.HIGH)
GPIO.output(RELAY_PIN, GPIO.LOW)
while True: # Run forever
    if GPIO.input(15) == GPIO.HIGH:
        print("Button was pushed!")
        GPIO.output(RELAY_PIN, GPIO.LOW)
        time.sleep(1)
    else:
        print("Released")
        GPIO.output(RELAY_PIN, GPIO.HIGH)
        time.sleep(1)
