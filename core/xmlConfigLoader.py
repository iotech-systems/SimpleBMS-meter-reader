
import os.path, typing as t
import xml.etree.ElementTree as et
from sbmslib.shared.core import ttyDeviceScanner as tds


MODBUS_PROCS_XML = "conf/modbusProcesses.xml"
STREAM_DEFS_XML = "streams/registerStreamDefinitions.xml"


class xmlConfigLoader(object):

   cache = {}

   def __init__(self):
      self.regStreamDefsXml: et.ElementTree = None
      self.modbusProcsXml: et.ElementTree = None

   @staticmethod
   def __confirm_conf_files__():
      for fn in (STREAM_DEFS_XML, STREAM_DEFS_XML):
         if not os.path.exists(fn):
            raise FileNotFoundError(fn)

   def loadConfXMLs(self) -> bool:
      try:
         xmlConfigLoader.__confirm_conf_files__()
         self.regStreamDefsXml = et.ElementTree().parse(STREAM_DEFS_XML)
         self.modbusProcsXml = et.ElementTree().parse(MODBUS_PROCS_XML)
         return True
      except FileNotFoundError as e:
         print(f"\n{e}\n\t--- stopping config loading process ---\n")
      except Exception as ex:
         print(f"loadConfXMLs ex: {ex}")

   def dump(self):
      print("\n--- loaded config elements ---")
      print(self.modbusProcsXml)
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

   def detectModbusAddressCollisions(self) -> tuple:
      xpath = "modbusProcess/meters/meter"
      meters: t.List[et.Element] = self.modbusProcsXml.findall(xpath)
      if len(meters) == 0:
         raise Exception("NoMetersFound!")
      ids = []; out = []
      for meter in meters:
         busAddress = int(meter.attrib["busAddress"])
         if busAddress not in ids:
            ids.append(busAddress)
         else:
            out.append(busAddress)
      # -- return --
      return tuple(out)

   """
      
   """
   def detectMeterSerialDevices(self):
      xpath = "modbusProcess"
      devScanner: tds.ttyUSBDeviceScanner
      modbusProcs: t.List[et.Element] = self.modbusProcsXml.findall(xpath)
      """
         each modbus process scans number of meters on a meter-data-bus
         each meter-data-bus is linked over serial port over usb ie: /dev/ttyUSBx 
      """
      for modbusProc in modbusProcs:
         try:
            print(f"\n\t-- pre-scanning: {modbusProc.attrib} --")
            ttyDev = modbusProc.attrib["ttyDevice"]
            if ttyDev.upper() == tds.ttyUSBDeviceScanner.AUTO:
               devScanner = tds.ttyUSBDeviceScanner()
               meters = modbusProc.findall("meters/meter")
               # -- should return dev string & update modbusProc xml --
               usbPort = devScanner.locateMetersUSBSerialPort(meters)
               if usbPort is None:
                  modbusProc.attrib["ttyDevice"] = "NotFound"
               else:
                  modbusProc.attrib["ttyDevice"] = usbPort.device
               # -- post scan --
               print(f"\t-- post-scanning: {modbusProc.attrib} --")
         except Exception as e:
            print(e)
