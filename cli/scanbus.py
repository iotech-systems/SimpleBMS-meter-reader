#!/usr/bin/env python3

import sys, time
import minimalmodbus as mm


if len(sys.argv) == 1:
   print("\n\t./scanbus.py /dev/ttyUSBx baudrate parity timeout")
   exit(0)

ttydev = sys.argv[1]
brate = int(sys.argv[2])
parity = sys.argv[3]
timeout = float(sys.argv[4])

inst = mm.Instrument(ttydev, 1)
inst.serial.baudrate = brate
inst.serial.parity = parity
inst.serial.timeout = timeout
inst.debug = True


def main():
   for i in range(10, 24):
      try:
         time.sleep(0.8)
         print(f"scanning address: {i}")
         inst.address = i
         val = inst.read_register(2)
         print(f" + response: {val}")
      except:
         print(" - no response!")


# - - - - - - - - - - - - - - - - - - - - - - - - -
if __name__ == "__main__":
    main()
