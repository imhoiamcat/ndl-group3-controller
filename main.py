from DoorDaemon import DoorDaemon

from RfidListenerDaemon import RfidListenerDaemon

from FileTransferDaemon import FileTransferDaemon

from LockAPi import LockAPi

from mqtt import MQTTServer

def main():
    # mqtt
    lock = LockAPi()
    
    mqtt = MQTTServer(lock)
    mqtt.run()
    
    # if face recognition fails, the tag can be used to authenticate
    rfid_daemon = RfidListenerDaemon(mqtt)
    rfid_daemon.run()

    # to handle openning the door
    door_daemon = DoorDaemon(lock)
    door_daemon.run()

    # to send log file
    file_daemon = FileTransferDaemon()
    file_daemon.run()
    

if __name__ == "__main__":
    main()