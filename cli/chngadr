#!/usr/bin/env python3

import sys
import minimalmodbus as mm


ttydev = sys.argv[1]
adrold = sys.argv[2]
adrnew = sys.argv[3]

inst = mm.Instrument(ttydev, 1)
inst.serial.baudrate = 9600
inst.serial.parity = "E"
inst.serial.timeout = 0.20
inst.debug = True


def main():
   inst.address = adrold
   inst.write_register(2, int(adrnew))
   val = inst.read_register(2)
   print(f"new adr: {val}")


# - - - - - - - - - - - - - - - - - - - - - - - - -
if __name__ == "__main__":
    main()
