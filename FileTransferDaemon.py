from datetime import datetime
import threading
from loguru import logger
from FileOperations import FileTransfer
from LockAPi import LockAPi

class FileTransferDaemon:
	def __init__(self):
		self.ft = FileTransfer("/home/ndl/ndl-project/mqtt.log")
		self.start = datetime.day

	def _run(self):
		while True:
			end = datetime.day
			if (end != self.start):
				self.ft.file_transfer()
				self.start = datetime.now()
				
			
	def run(self):	
		daemon_thread = threading.Thread(target=self._run)
		daemon_thread.start()

def main():
   daemon = FileTransferDaemon()
   daemon.run()
    
if __name__ == "__main__":
    main()