import paho.mqtt.subscribe as subscribe
import RPi.GPIO as GPIO
import time

# Set the GPIO mode (BCM or BOARD)
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin controlled the electromagnetic lock via the relay module
RELAY_PIN = 12

# Set the relay pin as an output pin
GPIO.setup(RELAY_PIN, GPIO.OUT)
	
while True:
	msg = subscribe.simple("mqtt/pimylifeup")
	print(msg.topic, msg.payload)
	if msg.payload == b'open':
		print("open")
		GPIO.output(RELAY_PIN, GPIO.LOW)
		time.sleep(2)
	else:
		print("close")
		GPIO.output(RELAY_PIN, GPIO.HIGH)
		time.sleep(2)
	
