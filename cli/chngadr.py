#!/usr/bin/env python3

import sys
import minimalmodbus as mm


# tty device
ttydev = sys.argv[1]
if ttydev == "?":
   print("chngadr /dev/ttyUSB? regadr oldadr newadr")
   exit(0)

# register holding modbus address
regadr: int = int(sys.argv[2])
# current modbus address value
adrold: int = int(sys.argv[3])
# new modbus address value
adrnew: int = int(sys.argv[4])


inst = mm.Instrument(ttydev, 1)
inst.serial.baudrate = 9600
inst.serial.parity = "E"
inst.serial.timeout = 0.20
inst.debug = True


def main():
   # set current modbus address
   inst.address = adrold
   # upload new address
   inst.write_register(regadr, adrnew)
   # change to new modbus address
   inst.address = adrnew
   val = inst.read_register(regadr)
   print(f"new adr: {val}")


# - - - - - - - - - - - - - - - - - - - - - - - - -
if __name__ == "__main__":
   main()
