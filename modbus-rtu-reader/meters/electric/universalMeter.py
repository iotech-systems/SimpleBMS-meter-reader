
import copy
import time
import minimalmodbus as mm
import meters.core as c
import meters.electric.register as r
import meters.electric.registerNames as rn
import meters.electric.meterLoader as ml
import data.models.dbMeterInfo as dbmi


READ_DELAY = 0.480

"""
   universal meter loads settings & register definitions & uses them
   to run meter readings 
"""


class universalMeter(object):

   # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
   def __init__(self, host: str = "", serPort: str = ""
                , meterInfo: dbmi.dbMeterInfo = None):
      # - - - - - - - - - - - -
      self.host: str = host
      self.serPort: str = serPort
      self.meterInfo: dbmi.dbMeterInfo = meterInfo
      self.modbusID = self.meterInfo.modbusID
      # load meter registers
      self.registers: tuple = \
         ml.meterLoader.loadRegisters(self.meterInfo.meterTag)
      if self.registers is None:
         raise Exception(f"BadMeterTag: {self.meterInfo.meterTag}")
      # load meter settings
      self.settings: c.SETTINGS = \
         ml.meterLoader.loadSettings(self.meterInfo.meterTag)
      self.settings.print()
      if self.settings is None:
         raise Exception(f"BadMeterTag: {self.meterInfo.meterTag}")
      # create meter instrument
      self.meterInst: mm.Instrument = \
         self.__create_instrument__()
      # scanned registers
      self.registersOut = []

   # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
   def readRegisters(self) -> []:
      try:
         regOut: r.register
         for register in self.registers:
            if not register.enable:
               continue
            regOut = self.__read_meter_field__(register)
            if regOut is None:
               print("\t -> regOut is None")
            else:
               regOut.print()
            # put into scanned
            self.registersOut.append(regOut)
         # - - - -
      except Exception as e:
         print(f"\n\t *** {e}")

   # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
   def confirmModbusID(self, modbusAdrID: int):
      addressReg: r.register = \
         self.__get_register_by_name__(rn.regsNames.ModbusAddress)
      # - - - - - -
      if addressReg is None:
         print("[ could not find ModbusAddress register! ]")
         return False
      # - - - - - -
      addressRegOut: r.register = self.__read_meter_field__(addressReg)
      return modbusAdrID == int(str(addressRegOut.regValue), 0)

   # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
   """
      ping is used to see if the meter is responding for now it will
      ask for a known value. madbus address id can be such a value
   """
   def ping(self) -> bool:
      return self.__check_address_id__(self.modbusID)

   # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
   def close(self):
      pass

   # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
   def __read_meter_field__(self, reg: r.register) -> r.register:
      try:
         time.sleep(READ_DELAY)
         regOut: r.register = copy.deepcopy(reg)
         print(f"\n >>> reading meter field: {reg.name} <<<\n")
         val = None
         # read register(s)
         if reg.mode == r.dataMode.rawRegister:
            if reg.size == 1:
               val = self.meterInst.read_register(reg.address, reg.decpnt)
            else:
               val = self.meterInst.read_registers(reg.address, reg.size)
         # read float
         if reg.mode == r.dataMode.numFloat:
            val = self.meterInst.read_float(reg.address, number_of_registers=reg.size)
         # read string
         if reg.mode == r.dataMode.strString:
            val = self.meterInst.read_string(reg.address, number_of_registers=reg.size)
         if reg.mode == r.dataMode.numInt:
            val = self.meterInst.read_long(reg.address)
         # - - - - -
         if regOut is not None:
            regOut.setRegValue(val)
         return regOut
      except Exception as e:
         return self.__retry_read_register__(reg)

   # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
   def __retry_read_register__(self, reg: r.register):
      try:
         time.sleep(READ_DELAY * 2)
         print(f"\n >>> retry reading meter field: {reg.name} <<<\n")
         regOut: r.register = copy.deepcopy(reg)
         self.meterInst.serial.baudrate = self.settings.baudrate
         val = self.meterInst.read_register(reg.address, reg.decpnt)
         regOut.setRegValue(val)
         return regOut
      except Exception as e:
         print(f"\t-> {e}")
         return None

   # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
   def __create_instrument__(self) -> mm.Instrument:
      meterInst: mm.Instrument = mm.Instrument(port=self.serPort
         , slaveaddress=self.modbusID, mode=mm.MODE_RTU, debug=False)
      # - - - -
      meterInst.serial.baudrate = self.settings.baudrate
      meterInst.serial.stopbits = self.settings.stopbits
      meterInst.serial.parity = self.settings.parity
      meterInst.serial.timeout = self.settings.timeout
      meterInst.clear_buffers_before_each_transaction = True
      if not meterInst.serial.is_open:
         meterInst.serial.open()
      # self.meterInst.precalculate_read_size = True
      # self.meterInst.close_port_after_each_call = True
      # print(self.meterInst.serial)
      return meterInst

   # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
   def __get_register_by_name__(self, regName: str):
      for reg in self.registers:
         if reg.name == regName:
            return reg

   # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
   def __check_address_id__(self, modbusAdrID: int) -> bool:
      addressReg: r.register = \
         self.__get_register_by_name__(rn.regsNames.ModbusAddress)
      # - - - - - -
      if addressReg is None:
         print("[ could not find ModbusAddress register! ]")
         return False
      # - - - - - -
      addressRegOut: r.register = self.__read_meter_field__(addressReg)
      if addressRegOut is not None:
         return modbusAdrID == int(str(addressRegOut.regValue), 0)
      else:
         return False
