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

    def close_lock(self):
        GPIO.output(self.RELAY_PIN, GPIO.LOW)

    def open_lock(self):
        GPIO.output(self.RELAY_PIN, GPIO.HIGH)    

    def get_lock_status(self):
        return GPIO.input(self.RELAY_PIN)    


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
