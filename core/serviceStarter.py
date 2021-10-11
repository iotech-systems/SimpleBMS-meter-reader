
from typing import List
import xml.etree.ElementTree as et
from core import xmlConfigLoader, modbusProcess
from core.sys import modbusAttrib


class serviceStarter(object):

   def __init__(self, conf: xmlConfigLoader.xmlConfigLoader):
      self.conf = conf
      self.modbusProcessors: List[modbusProcess.modbusProcess] = []

   def initLoad(self):
      self.__load_modbus_processors__()
      self.__init_modbus_processors__()

   def start(self) -> List[modbusProcess.modbusProcess]:
      self.__start_modbus_processors__()
      return self.modbusProcessors

   def __load_modbus_processors__(self):
      # get all modbusProcess xml nodes
      tag = "modbusProcess"
      procsDefs: List[et.Element] = self.conf.modbusProcsXml.findall(tag)
      for procDef in procsDefs:
         # start only those marked for start with yes
         if procDef.attrib[modbusAttrib.start].upper() == "YES":
            ttyDev = procDef.attrib["ttyDevice"]
            if ttyDev == "NotFound":
               print("serial device not found for modbusProcess:")
               print(f"\t{procDef.attrib}")
               continue
            # -- should run this process --
            self.modbusProcessors.append(modbusProcess.modbusProcess(procDef))

   def __init_modbus_processors__(self):
      for modProc in self.modbusProcessors:
         modProc.procInit()

   def __start_modbus_processors__(self):
      for modProc in self.modbusProcessors:
         modProc.start()
