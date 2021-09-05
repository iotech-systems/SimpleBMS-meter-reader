
import time
import requests as rq
from core import modbusProcess
from typing import List
import conf.restapi as s


MONITOR_LOOP_DELAY_SECS: int = 120


class serviceMonitorLoop(object):

   def __init__(self, modbusProcs: List[modbusProcess.modbusProcess]):
      self.modbusProcs = modbusProcs

   def run(self):
      while True:
         print(f"\t\t[ main monitor loop delay: {MONITOR_LOOP_DELAY_SECS} secs ]")
         time.sleep(MONITOR_LOOP_DELAY_SECS)
         self.__run__()

   def __run__(self):
      try:
         self.__dump_sys_procs__()
         for proc in self.modbusProcs:
            print(proc)
         # ping REST server
         self.__ping__()
      except Exception as e:
         print(e)

   def __dump_sys_procs__(self):
      for proc in self.modbusProcs:
         print(f"\t\tpid: {proc.pid}")

   def __ping__(self):
      try:
         with open("/etc/hostname", "r") as file:
            hn = file.readline().strip()
         url: str = f"http://{s.SBMS_REST_SERVER}/{s.REST_REPORT_PING_URL}?hostname={hn}"
         res: rq.Response = rq.get(url)
         print(res.content.decode("utf-8"))
      except IOError as e:
         print(e)
