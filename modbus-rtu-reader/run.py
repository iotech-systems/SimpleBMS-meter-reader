#!/usr/xbin/env python3

import time
import multiprocessing as mp
import setproctitle
import serviceConfig
import modbusScanner


SYS_PROCS = []
PROC_NAME = "iot-sbms-main"


def validateConfig():
   serviceConfig.serviceConfig.dump()
   if not testSerialPorts(serviceConfig.serviceConfig.ttyPorts):
      pass


def testSerialPorts(ttyPorts: tuple):
   for ttyPort in ttyPorts:
      print(ttyPort)
   return True


def startModbusScanners():
   serPortDevs = serviceConfig.serviceConfig.meters.keys()
   for serPort in serPortDevs:
      # create object
      meters = serviceConfig.serviceConfig.meters[serPort]
      # print(meters)
      if meters is None or len(meters) == 0:
         print(f"\n -> skipping port: {serPort}\n")
         continue
      # - - - - - - - -
      _modbusScanner = modbusScanner.modbusScanner(serPort, meters)
      # create & start process
      proc = mp.Process(target=_modbusScanner.run)
      proc.start()
      global SYS_PROCS
      SYS_PROCS.append(proc)
      time.sleep(2.0)
   return


def monitorLoop():
   while True:
      try:
         print(f"\n\t--- monitor loop ---\n\tsys_procs:")
         dump_sys_procs()
         time.sleep(16.0)
      except Exception as e:
         pass


def dump_sys_procs():
   for p in SYS_PROCS:
      p: mp.Process = p
      print(f"\t\tpid: {p.pid}")


def main():
   # set main process name
   setproctitle.setproctitle(PROC_NAME)
   print("\n\t[ -- main -- ]")
   validateConfig()
   startModbusScanners()
   monitorLoop()


# - - - - - - entry point - - - - - -
if __name__ == "__main__":
   main()
