import time
from pirc522 import RFID
from LockAPi import LockAPi
import threading 

class RfidDaemon:
    def __init__(self, lock):
        self.lock = lock
        self.rdr = RFID()
        self.util = self.rdr.util()

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
                        self.util.set_tag(uid)
                        # authenticate
                        self.util.auth(self.rdr.auth_a, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
                        # if authenticated open lock
                        self.lock.open_lock()
                        time.sleep(5)
                        self.lock.close_lock()
                        self.util.deauth()
                        time.sleep(1)

        except KeyboardInterrupt:
            print('interrupted!')

    def run(self):
        daemon_thread = threading.Thread(target=self._run)
        daemon_thread.start()

# to test the rfid daemon
def main():
   lock = LockAPi()
   daemon = RfidDaemon(lock)
   daemon.run()
    
if __name__ == "__main__":
    main()