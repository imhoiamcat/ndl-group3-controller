import time
from pirc522 import RFID
from LockAPi import LockAPi
from mqtt import MQTTServer
import threading 
import hashlib

class RfidListenerDaemon:
    def __init__(self, mqtt_server:MQTTServer):
        self.mqtt_server = mqtt_server
        self.rdr = RFID()

    def _run(self):
        try:
            while True:
                self.rdr.wait_for_tag()
                (error, data) = self.rdr.request()
                if not error:
                    print("\ndetected")
                    (error, uid) = self.rdr.anticoll()
                    if not error:
                        print(str(uid))
                        hashed_uid = hashlib.sha256(str(uid).encode()).hexdigest()
                        self.mqtt_server.send_message(hashed_uid, "rfid")

        except KeyboardInterrupt:
            print('interrupted!')

    def run(self):
        daemon_thread = threading.Thread(target=self._run)
        daemon_thread.start()

# to test the rfid daemon
def main():
   lock = LockAPi()
   mqtt = MQTTServer(lock)
   daemon = RfidListenerDaemon(mqtt)
   daemon.run()
    
if __name__ == "__main__":
    main()