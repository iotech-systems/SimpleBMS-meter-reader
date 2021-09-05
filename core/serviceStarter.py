
from typing import List
from core import xmlConfigLoader, modbusProcess
from core.sys import modbusAttrib


class serviceStarter(object):

   def __init__(self, conf: xmlConfigLoader.xmlConfigLoader):
      self.conf = conf
      self.modbusProcessors: List[modbusProcess.modbusProcess] = []

   def loadInit(self):
      self.__load_modbus_processors__()
      self.__init_modbus_processors__()

   def start(self) -> List[modbusProcess.modbusProcess]:
      self.__start_modbus_processors__()
      return self.modbusProcessors

   def __load_modbus_processors__(self):
      procsDefs: [] = self.conf.startConfXml.findall("modbusProcess")
      for procDef in procsDefs:
         # start only those marked for start with yes
         if procDef.attrib[modbusAttrib.start].upper() == "YES":
            self.modbusProcessors.append(modbusProcess.modbusProcess(procDef))

   def __init_modbus_processors__(self):
      for modProc in self.modbusProcessors:
         modProc.procInit()

   def __start_modbus_processors__(self):
      for modProc in self.modbusProcessors:
         modProc.start()
