import threading 

import RPi.GPIO as GPIO

import time

from LockAPi import LockAPi

class DoorDaemon:
	def __init__(self, lock):
		self.lock = lock

	def _run(self):
		while True:
			if self.lock.get_lock_status():
				time.sleep(15)
				self.lock.close_lock()
			
	def run(self):	
		daemon_thread = threading.Thread(target=self._run)
		daemon_thread.start()

# to test the door daemon
def main():
   lock = LockAPi()
   lock.open_lock()
   daemon = DoorDaemon(lock)
   daemon.run()
    
if __name__ == "__main__":
    main()
