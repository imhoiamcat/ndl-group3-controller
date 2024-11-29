from lib2to3.pgen2.tokenize import endprogs

import paho.mqtt.client as mqtt
import time
import threading
import RPi.GPIO as GPIO

from loguru import logger
import sys

# Set the GPIO mode (BCM or BOARD)
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin controlled the electromagnetic lock via the relay module
RELAY_PIN = 12

# Set the relay pin as an output pin
GPIO.setup(RELAY_PIN, GPIO.OUT)

class MQTTServer:
    def __init__(self):
        # self._endpoints = Endpoints()
        # MQTT server config
        # broker here is the mosquito broker running on the pi
        self._broker = "localhost"
        self._port = 1883
        self._topic = "weird-stuff"
        
        # set up MQTT client
        self._client = mqtt.Client()
        self._client.username_pw_set("pico", "ndl@group3")
        self._client.on_message = self._on_message
        self._connect()
        
        # subscribe to the topic I need to listen to
        self._client.subscribe("magnetic_lock")
        
        # configure log format
        logger.remove(0)
        logger.add(sys.stderr, serialize=True)
      
        
    @classmethod
    def _on_message(cls, client, userdata, msg):
        match msg.topic:
            case "":
                payload = msg.payload.decode()
            case "magnetic_lock":
                payload = msg.payload.decode()
                if payload == "close":
                    GPIO.output(RELAY_PIN, GPIO.LOW)
                    
                    # logging
                    if not GPIO.input(RELAY_PIN):
                        logger.success("The lock closed successfully.")
                    else:
                        logger.error("The lock close failed.")
                    client.publish(str(logger), "logs")
                    
                    # wait
                    time.sleep(2)
                else:
                    GPIO.output(RELAY_PIN, GPIO.HIGH)
                    
                    # logging
                    if GPIO.input(RELAY_PIN):
                        logger.success("The lock opened successfully.")
                    else:
                        logger.error("The lock open failed.")
                    client.publish(str(logger), "logs")
                    
                    # wait
                    time.sleep(2)
            case _:
                pass


    def _connect(self):
        self._client.connect(self._broker, self._port)


    def _mqtt_loop(self):
        self._client.loop_start()
        
    def send_message(self, message, topic=None):
        if not topic:
            topic = self._topic
        self._client.publish(topic, message)
        
    # subscriber; topic: logs
    def logs_dump(self):
        pass


    def _run(self):
        self._mqtt_loop()
        try:
            while True:
                # self.send_message(str(logger), "logs")
                time.sleep(1)
        except KeyboardInterrupt:
            print("Publisher stopped")
        self._client.loop_stop()
        self._client.disconnect()

    def run(self):
        server_thread = threading.Thread(target=self._run)
        server_thread.start()


def main():
    mqtt = MQTTServer()
    mqtt.run()
    
    
if __name__ == "__main__":
    main()
