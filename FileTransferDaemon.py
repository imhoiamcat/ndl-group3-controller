from datetime import datetime
import threading
from FileOperations import FileTransfer

class FileTransferDaemon:
	def __init__(self):
		self.ft = FileTransfer("/home/ndl/ndl-project/mqtt.log")
		self.start = datetime.now().minute

	def _run(self):
		while True:
			end = datetime.now().minute
			if (end != self.start):
				self.ft.file_transfer()
				self.start = datetime.now().minute
				
			
	def run(self):	
		daemon_thread = threading.Thread(target=self._run)
		daemon_thread.start()

def main():
   daemon = FileTransferDaemon()
   daemon.run()
    
if __name__ == "__main__":
    main()