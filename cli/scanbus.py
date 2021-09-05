#!/usr/bin/env python3

import sys
import minimalmodbus as mm


ttydev = sys.argv[1]
brate = sys.argv[2]
parity = sys.argv[3]

inst = mm.Instrument(ttydev, 1)
inst.serial.baudrate = brate
inst.serial.parity = parity
inst.serial.timeout = 0.25
inst.debug = True


def main():
   for i in range(1, 20):
      try:
         inst.address = i
         val = inst.read_register(2)
         print(f"val: {val}")
      except:
         pass


# - - - - - - - - - - - - - - - - - - - - - - - - -
if __name__ == "__main__":
    main()
