
import time, json
from typing import List
import xml.etree.ElementTree as xmlTree
from core import streamJobBase, xmlConfigLoader, actions
from core.sys import jobXmlAttrib, meterXmlAttrib
from meters.electric import modbusBasedMeter as mbm
from meters.electric.meterFieldReading import meterFieldReading
from ommslib.shared.utils.jsonPackageMaker import jsonPackageMaker


INNER_METER_DELAY = 0.333


class registerStreamJob(streamJobBase.streamJobBase):

   def __init__(self, xmlJob: xmlTree.Element):
      print("\n\n[ c-tor: registerStreamJob ]")
      super(registerStreamJob, self).__init__(xmlJob)
      self.kwargs = None

   def run(self, **kwargs) -> int:
      self.kwargs = kwargs
      # - - - -
      try:
         meters = None; ttyDevice = ""
         # -- get list of the meters attached to this modbus --
         if "meters" in kwargs.keys():
            meters: xmlTree.Element = kwargs["meters"]
         if "ttyDevice" in kwargs.keys():
            ttyDevice = kwargs["ttyDevice"]
         # - - - - -
         print(f"running job: {self.xmlJob.attrib} on: {ttyDevice}")
         # - - - - -
         meterInfoList: List[xmlTree.Element] = meters.findall("meter")
         if len(meterInfoList) == 0:
            return 1
         # -- read stream type --
         streamType = self.xmlJob.attrib[jobXmlAttrib.streamType]
         xmlConf: xmlConfigLoader.xmlConfigLoader = xmlConfigLoader.xmlConfigLoader()
         streamRegsXml: xmlTree.Element = xmlConf.getStreamTypeRegisters(streamType)
         # -- run over all meters attached to the bus --
         for meterInfo in meterInfoList:
            meterInfo.attrib["ttyDevice"] = ttyDevice
            meterFields = self.__runMeter__(meterInfo, streamRegsXml)
            self.__checkMeterOutput__(meterFields)
            time.sleep(INNER_METER_DELAY)
         # -- end loop --
         return True
      except Exception as e:
         print(e.__traceback__)

   def __runMeter__(self, meter: xmlTree.Element, streamRegsXml: xmlTree.Element) \
         -> [List[meterFieldReading], False]:
      try:
         busAdr = int(meter.attrib[meterXmlAttrib.busAddress])
         brand = meter.attrib[meterXmlAttrib.brand]
         modelXmlFile = meter.attrib[meterXmlAttrib.modelXML]
         ttyDevice = meter.attrib["ttyDevice"]
         # - - load meter xml - -
         xmlConf: xmlConfigLoader.xmlConfigLoader = xmlConfigLoader.xmlConfigLoader()
         modelXml = xmlConf.getMeterModelXml(brand, modelXmlFile)
         modbusMeter: mbm.modbusBasedMeter = mbm.modbusBasedMeter(host="", ttyDev=ttyDevice
            , modbusAddress=busAdr, streamRegNames=streamRegsXml, meterXml=modelXml)
         modbusMeter.initMeter()
         if not modbusMeter.ping():
            return False
         # -- meter found start reading --
         starTime = time.time()
         readings: List[meterFieldReading] = modbusMeter.readMappedFieldsStreamFrame()
         readTime = round((time.time() - starTime), 3)
         lstReadings = self.__readingsAsList(readings)
         jsonPackage = self.__createMeterJsonPackage__(busAdr, readTime, lstReadings
            , modelXml, streamRegsXml)
         actions.actions.send2streamer(jsonPackage)
         # -- return readings --
         return readings
      except Exception as e:
         print(e)

   def __readingsAsList(self, readings: List[meterFieldReading]) -> List[dict]:
      buff = []
      for reading in readings:
         buff.append(reading.toDict())
      return buff

   def __checkMeterOutput__(self, readings: [List[dict], False]):
      if readings is False:
         # print("Meter field reading is False")
         return
      # - - - - -
      print("__checkMeterOutput__")
      buff = []
      for reading in readings:
         buff.append(reading.toDict())
      jsonBuff = json.dumps(buff)
      # print(jsonBuff)

   def __createMeterJsonPackage__(self, busAdr: int, readTime: float, readings: List[dict]
         , modelXml: xmlTree.Element, streamRegsXml: xmlTree.Element) -> str:
      # info about the stream, meter
      streamName = streamRegsXml.attrib["streamName"]
      streamTable = streamRegsXml.attrib["streamTbl"]
      meterBrand = modelXml.attrib["brand"]
      meterModel = modelXml.attrib["model"]
      # print(streamName, streamTable)
      # print(f"w: {self.xmlJob.attrib}")
      jpm: jsonPackageMaker = jsonPackageMaker()
      # - - - - -
      package = jpm.make(streamName, streamTable, meterBrand
         , meterModel, busAdr, readTime, readings)
      jsonBuff = json.dumps(package)
      # print(f"\tpackage: {jsonBuff}")
      return jsonBuff

   def __put_2_streamer__(self, jsonPackage: str):
      res = actions.actions.send2streamer(jsonPackage)
      print(f"res: {res}")
