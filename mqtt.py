import paho.mqtt.client as mqtt
import threading

from loguru import logger

from DoorDaemon import DoorDaemon

from FileTransferDaemon import FileTransferDaemon

from LockAPi import LockAPi

class MQTTServer:
    def __init__(self, lock: LockAPi):
        # MQTT server config
        # broker here is the mosquito broker running on the pi
        self._broker = "192.168.1.75"
        # self._broker = "100.100.6.68" 
        self._port = 1883
        self._topic = "weird-stuff"
        
        # set up MQTT client
        self._client = mqtt.Client()
        # self._client.username_pw_set("app", "ndl@group3")
        self._client.username_pw_set("server", "ndl@group3")
        self._client.on_message = self._on_message
        self._connect()
        
        # subscribe to the topics I need to listen to
        self._client.subscribe("magnetic_lock")
        
        # configure log format
        logger.remove(0)
        logger.add("mqtt.log", serialize=True)

        # set lock to the lock passed
        self.lock = lock
        

    def _on_message(self, client, userdata, msg):
        match msg.topic:
            case "magnetic_lock":
                self.handle_lock(msg)
            case _:
                pass


    def _connect(self):
        try:
            self._client.connect(self._broker, self._port)
            logger.success("MQTT server launched successfully.")
        except:
            logger.error("MQTT server launch failed.")
            

    def _mqtt_loop(self):
        self._client.loop_start()
        

    def send_message(self, message, topic=None):
        if not topic:
            topic = self._topic
        self._client.publish(topic, message)


    def handle_lock(self, msg):
        payload = msg.payload.decode()
        if payload == "close":
            self.lock.close_lock()      
            # logging
            if not self.lock.get_lock_status():
                logger.success("The lock closed successfully.")
            else:
                logger.error("The lock close failed.")

        elif payload == "open":
            self.lock.open_lock() 
            # logging
            if self.lock.get_lock_status():
                logger.success("The lock opened successfully.")
            else:
                logger.error("The lock open failed.")

            # sent lock status
            self.send_message(self.lock.get_status(), "lock")


    def _run(self):
        self._mqtt_loop()
        try:
            while True:
                pass
        except KeyboardInterrupt:
            print("Publisher stopped")
        self._client.loop_stop()
        self._client.disconnect()

    def run(self):
        server_thread = threading.Thread(target=self._run)
        server_thread.start()


def main():
    # mqtt
    lock = LockAPi()
    mqtt = MQTTServer(lock)
    mqtt.run()

    # to handle openning the door
    door_daemon = DoorDaemon(lock)
    door_daemon.run()

    # to send log file
    file_daemon = FileTransferDaemon()
    file_daemon.run()
    
if __name__ == "__main__":
    main()
