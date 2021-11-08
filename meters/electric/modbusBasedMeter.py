
__author__ = "Owsiak, Erik"
__license__ = "not sure yet"
__url__ = "https://github.com/url"
__version__ = "0.0.1"

import datetime, time
from typing import List
import xml.etree.ElementTree as et
import minimalmodbus as mm
from meters.electric import register, meterSerial
from ommslib.shared.core import registerNames
from meters.electric.register import register
from meters.electric.registerDataMode import registerDataMode
from meters.electric.meterFieldReading import meterFieldReading
from meters.electric.meterFieldsDefs import meterDataFields

READ_DELAY = 0.480

"""
   universal meter loads settings & register definitions & uses them
   to run meter readings 
"""


class modbusBasedMeter(object):

   # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
   def __init__(self, host: str = "", ttyDev: str = "", modbusAddress: int = 248
                , streamRegNames: et.Element = None, meterXml: et.Element = None):
      print("\n[ c-tor: modbusBasedMeter ]\n")
      # - - - - - - - - - - - -
      self.host: str = host
      self.ttyDevice: str = ttyDev
      self.modbusAddress = modbusAddress
      # subset of register names use during meter scan/stream
      self.streamRegNames: et.Element = streamRegNames
      self.meterXml: et.Element = meterXml
      # load meter settings
      self.meterSerial: meterSerial.meterSerial = None
      # create meter instrument
      self.meterInst = None
      # scanned registers
      self.registersOut = []

   def initMeter(self) -> None:
      try:
         # -- set modbus address register --
         serXml = self.meterXml.find("serial")
         self.meterSerial = meterSerial.meterSerial(serXml)
         self.meterInst: mm.Instrument = self.__createInstrument__()
      except Exception as e:
         print(f"initMeter: {e}")

   # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
   def readMappedFieldsStreamFrame(self) -> [List[meterFieldReading], False]:
      try:
         readings: List[meterFieldReading] = []
         """ -- scan data fields in this stream --
            this loop runs over a list of stream register names stored in xml file and 
            tagged with ~> streamName='kWhrs' registerStreamDefinitions.xml; this register 
            name is mapped to an xml file storing meter registers & addresses """
         for fieldNameElmt in self.streamRegNames.findall("streamField"):
            registerName = fieldNameElmt.attrib["name"]
            # placeholder value if field not mapped in meter xml
            notMappedVal = fieldNameElmt.attrib["notMappedValue"]
            xpath = f"registers/register[@name=\"{registerName}\"]"
            """ look up meter register info in meter xml file by register name in above
               it could be that the register might not exist in a meter model then
               create fake/placeholder register to enter default data into target db table 
               this mostly done so that reads from 1-phase meter can stored in single table
               with 3-phase meters"""
            registerXml: et.Element = self.meterXml.find(xpath)
            meterReading = None
            if registerXml is None:
               """ create fake register read with default value if reg not found to fill
                  database table row """
               fieldInfo = meterDataFields.getMeterDataFieldInfo(registerName)
               if fieldInfo is not False:
                  meterReading = meterFieldReading(regName=registerName, regVal=notMappedVal
                     , regValUnit=fieldInfo.fieldUnit, fldRegMapped=False)
               else:
                  print(f"RegisterName: {registerName} missing map!")
            else:
               meterRegister: register = register(registerXml)
               meterReading = self.__readMeterField__(meterRegister)
            # - - - -
            readings.append(meterReading)
         # -- return all readings --
         return readings
      except Exception as e:
         print(f"\n\t *** {e}")
         return False

   # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
   """
      ping is used to see if the meter is responding for now it will
      ask for a known value. madbus address id can be such a value
   """
   def ping(self) -> bool:
      rval = self.__checkAddressID__(self.modbusAddress)
      if not rval:
         print(f"\tPING {self.modbusAddress}: NoResponse!")
      else:
         print(f"\tPING {self.modbusAddress}: PONG OK!")
      # - - - - -
      return rval

   # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
   def close(self):
      pass

   # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
   def __readMeterField__(self, reg: register, maxRetries: int = 3) -> meterFieldReading:
      try:
         self.meterInst.serial.timeout = self.meterSerial.timeout
         returnVal = None
         # read register(s)
         if reg.mode == registerDataMode.rawRegister:
            if reg.size == 1:
               returnVal = self.meterInst.read_register(reg.address, reg.decpnt)
            else:
               returnVal = self.meterInst.read_registers(reg.address, reg.size)
         # read float
         if reg.mode == registerDataMode.numFloat:
            returnVal = self.meterInst.read_float(reg.address, number_of_registers=reg.size)
         # read string
         if reg.mode == registerDataMode.strString:
            returnVal = self.meterInst.read_string(reg.address, number_of_registers=reg.size)
         # read int
         if reg.mode == registerDataMode.numInt:
            returnVal = self.meterInst.read_long(reg.address)
         # -- meter was read -> create meter reading output --
         meterReading: meterFieldReading = meterFieldReading(regName=reg.name
            , regVal=returnVal, regValUnit=reg.unit, formatterName=reg.formatFuncName)
         # - - - - -
         return meterReading
      except Exception as x:
         print(f"x: {x}")
         if maxRetries > 0:
            nextMaxRetries: int = maxRetries - 1
            print(f"nextMaxTries: {nextMaxRetries}")
            return self.__readMeterField__(reg=reg, maxRetries=nextMaxRetries)
         print(f"\tGiving up! ~> {reg.name} MaxTries")
         meterReading: meterFieldReading = \
            meterFieldReading(regName=reg.name, regVal=None, regValUnit="", errorReading=True)
         return meterReading

   # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
   def __createInstrument__(self) -> mm.Instrument:
      # - - - - -
      meterInst: mm.Instrument = mm.Instrument(port=self.ttyDevice
         , slaveaddress=self.modbusAddress, mode=mm.MODE_RTU, debug=False)
      if meterInst is None:
         raise Exception("unable to create instrument")
      # - - - - -
      meterInst.serial.baudrate = self.meterSerial.baudrate
      meterInst.serial.stopbits = self.meterSerial.stopbits
      meterInst.serial.parity = self.meterSerial.parity
      meterInst.serial.timeout = self.meterSerial.timeout
      meterInst.clear_buffers_before_each_transaction = True
      # - - - -
      if not meterInst.serial.is_open:
         meterInst.serial.open()
      # self.meterInst.precalculate_read_size = True
      # self.meterInst.close_port_after_each_call = True
      return meterInst

   # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
   def __checkAddressID__(self, modbusAddress: int) -> bool:
      addressReg: register = \
         self.__getRegisterByName__(registerNames.registerNames.ModbusAddress)
      # - - - - - -
      if addressReg is None:
         print("[ could not find ModbusAddress register! ]")
         return False
      # - - - - - -
      reading: meterFieldReading = self.__readMeterField__(addressReg)
      if not reading.hasError:
         return modbusAddress == int(str(reading.regVal), 0)
      else:
         return False

   def __getRegisterByName__(self, regName: str) -> [register, None]:
      xpath = f"registers/register[@name=\"{regName}\"]"
      regXml: et.Element = self.meterXml.find(xpath)
      if regXml is None:
         return None
      reg: register = register(regXml)
      return reg

   # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
   def __load_meter_settings__(self):
     pass

   def __set_meter_name__(self):
      with open("/etc/hostname", "r") as file:
         buff: str = file.read()
      return buff.strip()
