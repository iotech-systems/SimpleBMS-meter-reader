
"""
   this class runs as process and monitors single tty device
"""
import time
import datetime as dt
import setproctitle
import xml.etree.ElementTree as etXml
from typing import List
from threading import Thread
from multiprocessing import Process
from core.sys import jobXmlAttrib, xmlConsts, dtsFormats
from jobs import registerStreamJob as rsj


class modbusProcess(Process):

   """
      this should take a tuple of stream threads definitions
      will need a way to schedule a stream thread to run
   """
   def __init__(self, xmlElmnt: etXml.Element):
      super().__init__(daemon=True)
      # - - - - - - - - -
      print(f"\n[ c-tor: modbusProcess ]\n")
      self.xmlConf: etXml.Element = xmlElmnt
      self.id: str = self.xmlConf.attrib["id"].strip()
      self.tag: str = self.xmlConf.attrib["tag"].strip()
      self.ttyDevice = self.xmlConf.attrib["ttyDevice"].strip()
      self.processorJobs: List[etXml.Element] = []
      self.processorMeters = None
      self.monitorThread = None
      self.errorDelaySecs = 60.0
      # set process name
      self.name = f"modbusProcess: [{self.ttyDevice}]"

   def procInit(self):
      # -- load modbus meters ---
      xpath = "meters"
      self.processorMeters: etXml.Element = self.xmlConf.find(xpath)
      # - - create processor jobs table - -
      xpath = "processorJobs"
      self.processorJobs: etXml.Element = self.xmlConf.find(xpath)
      # - - add runtime needed tags - -
      xpath = "job"
      for job in self.processorJobs.findall(xpath):
         job.attrib[jobXmlAttrib.lastRunStartDTS] = xmlConsts.unknown
         job.attrib[jobXmlAttrib.lastRunEndDTS] = xmlConsts.unknown

   def run(self) -> None:
      try:
         setproctitle.setproctitle("modbus-scanner")
         # - - start monitor thread - -
         if not self.__start_monitor_thread__():
            print("unable to start modbus processor thread loop")
         # - - start main processor loop --
         self.__mainLoop__()
      except Exception as e:
         print(e)

   def __start_monitor_thread__(self) -> bool:
      try:
         threadName = f"monitorThread: {self.ttyDevice}"
         self.monitorThread: Thread = Thread(name=threadName, target=self.__monitor_thread__)
         self.monitorThread.start()
         return True
      except Exception as e:
         print(e)
         return False

   def __monitor_thread__(self):
      while True:
         try:
            print(f"\n\t-- modbusProcessorMonitor: {self.ttyDevice} --\n")
         except Exception as e:
            print(e)
         finally:
            time.sleep(32.0)
      # - - - - - - - -

   def __mainLoop__(self):
      print(f"\t-- modbusProcess: calling __main_loop__: {self.ttyDevice} --")
      while True:
         try:
            # per each job
            for job in self.processorJobs:
               if modbusProcess.__isTimeToRun__(job):
                  self.__runJob__(job)
               # inner jobs delay
               time.sleep(0.20)
            # - - - -
            print(" -> modbusProcess: loop <- ")
            time.sleep(1.0)
         except Exception as e:
            print(e)

   def __runJob__(self, job: etXml.Element):
      try:
         utcNow = dt.datetime.utcnow().strftime(dtsFormats.std)
         job.attrib[jobXmlAttrib.lastRunStartDTS] = utcNow
         registerJob: rsj.registerStreamJob = rsj.registerStreamJob(job)
         if registerJob is None:
            print("registerJob is None!!!")
            return
         # -- this will run job in box --
         registerJob.run(meters=self.processorMeters, ttyDevice=self.ttyDevice)
         utcNow = dt.datetime.utcnow().strftime(dtsFormats.std)
         job.attrib[jobXmlAttrib.lastRunEndDTS] = utcNow
      except Exception as e:
         print(f"e: {e}")

   @staticmethod
   def __isTimeToRun__(job: etXml.Element) -> bool:
      try:
         startBuff = job.attrib[jobXmlAttrib.lastRunStartDTS]
         if startBuff.strip() == xmlConsts.unknown.strip():
            return True
         # - - - - - - -
         lastRunDts: dt.datetime = dt.datetime.strptime(startBuff, dtsFormats.std)
         diffSecs = (dt.datetime.utcnow() - lastRunDts).total_seconds()
         return (diffSecs / 60) > int(job.attrib[jobXmlAttrib.intervalMins])
         # - - - - - - -
      except Exception as e:
         print(e)
         return False

   def __job_info__(self, job: etXml.Element):
      print("\n\t- - - running job - - -")
      print(f"\tmodbusProcess ~ id: {self.id} ~ tag: {self.tag} ~ ttyDev: {self.ttyDevice}")
      print(job.attrib)
