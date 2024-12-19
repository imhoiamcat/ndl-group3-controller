import RPi.GPIO as GPIO
import time

class LockAPi:
    def __init__(self):
        # Set the BCM GPIO mode
        GPIO.setmode(GPIO.BOARD)
        # Define the GPIO pin controlled the electromagnetic lock via the relay module
        self.RELAY_PIN = 32
        GPIO.setup(self.RELAY_PIN, GPIO.OUT)
        # When just created set lock to close
        GPIO.output(self.RELAY_PIN, GPIO.LOW)
        self.status = 0

    def close_lock(self):
        if (self.status):
            GPIO.output(self.RELAY_PIN, GPIO.LOW)
            self.status = 0

    def open_lock(self):
        if not self.status:
            GPIO.output(self.RELAY_PIN, GPIO.HIGH)    
            self.status = 1

    def get_lock_status(self):
        return self.status

    def get_status(self):
        if self.status:
            return "open"
        else:
            return "close" 


# to test the lock APi
def main():
   lock = LockAPi()
   lock.close_lock()
   time.sleep(1)
   lock.open_lock()
   time.sleep(1)
   lock.close_lock()
    

if __name__ == "__main__":
    main()
