import time
from pirc522 import RFID

rdr = RFID()
util = rdr.util()

# util.debug = True

try:
    while True:
        rdr.wait_for_tag()
        (error, data) = rdr.request()
        if not error:
            print("\ndetected")
            (error, uid) = rdr.anticoll()
            if not error:
                print("Card uid:" + str(uid))
                util.set_tag(uid)
                util.auth(rdr.auth_a, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
                util.deauth()
                time.sleep(1)

except KeyboardInterrupt:
  print('interrupted!')