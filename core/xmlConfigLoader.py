
import os.path
import xml.etree.ElementTree as et


START_CONF_XML = "conf/sbmsModbusProcesses.xml"
STREAM_DEFS_XML = "streams/registerStreamDefinitions.xml"


class xmlConfigLoader(object):

   cache = {}

   def __init__(self):
      self.regStreamDefsXml: et.ElementTree = None
      self.startConfXml: et.ElementTree = None

   @staticmethod
   def __confirm_conf_files__():
      for fn in (STREAM_DEFS_XML, STREAM_DEFS_XML):
         if not os.path.exists(fn):
            raise FileNotFoundError(fn)

   def loadConfXMLs(self) -> bool:
      try:
         xmlConfigLoader.__confirm_conf_files__()
         self.regStreamDefsXml = et.ElementTree().parse(STREAM_DEFS_XML)
         self.startConfXml = et.ElementTree().parse(START_CONF_XML)
         return True
      except FileNotFoundError as e:
         print(f"\n{e}\n\t--- stopping config loading process ---\n")
      except Exception as ex:
         print(f"loadConfXMLs ex: {ex}")

   def dump(self):
      print("\n--- loaded config elements ---")
      print(self.startConfXml)
      print(self.regStreamDefsXml)

   def getStreamTypeRegisters(self, streamType: str) -> et.Element:
      try:
         if streamType in xmlConfigLoader.cache:
            return xmlConfigLoader.cache[streamType]
         # - - - - -
         # streamRegister streamName="kWhrs" streamTbl="stream.kwhrs"
         self.loadConfXMLs()
         xpath = f"streamRegisters[@streamName=\"{streamType}\"]"
         xmlElm: et.Element = self.regStreamDefsXml.find(xpath)
         if xmlElm is not None:
            xmlConfigLoader.cache[streamType] = xmlElm
         return xmlConfigLoader.cache[streamType]
      except Exception as e:
         print(e.__traceback__)

   def getMeterModelXml(self, brand: str, modelXml: str) -> et.Element:
      # - - - - -
      fn = f"brands/{brand}/{modelXml}"
      if fn in xmlConfigLoader.cache:
         return xmlConfigLoader.cache[fn]
      # - - - - -
      if not os.path.exists(fn):
         raise FileNotFoundError(fn)
      # - - - - -
      tmpXml = et.ElementTree().parse(fn)
      xmlConfigLoader.cache[fn] = tmpXml
      return xmlConfigLoader.cache[fn]
