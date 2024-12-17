import time
from pirc522 import RFID
from LockAPi import LockAPi
from mqtt import MQTTServer
import threading 

class RfidListenerDaemon:
    def __init__(self, mqtt_server:MQTTServer):
        self.mqtt_server = mqtt_server
        self.rdr = RFID()
        #self.util = self.rdr.util()

    def _run(self):
        try:
            while True:
                self.rdr.wait_for_tag()
                (error, data) = self.rdr.request()
                if not error:
                    print("\ndetected")
                    (error, uid) = self.rdr.anticoll()
                    if not error:
                        # print("Card uid:" + str(uid))
                        # self.util.set_tag(uid)
                        # self.util.auth(self.rdr.auth_a, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
                        print(str(uid))
                        self.mqtt_server.send_message(str(uid), "rfid")
                        # self.util.deauth()

        except KeyboardInterrupt:
            print('interrupted!')

    def run(self):
        daemon_thread = threading.Thread(target=self._run)
        daemon_thread.start()

# to test the rfid daemon
def main():
   mqtt = MQTTServer()
   daemon = RfidListenerDaemon(mqtt)
   daemon.run()
    
if __name__ == "__main__":
    main()