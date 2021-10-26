
__author__ = "Owsiak, Erik"
__license__ = "not sure yet"
__url__ = "https://github.com/url"
__version__ = "0.0.1"

"""
      these are lookup tables for tagging registers in any meter
"""

from typing import List
from meters.electric.registerUnits import registerUnits as ru
from openbmslib.shared.core.registerNames import registerNames as rn


class meterDataField(object):
   """
      this class holds the basic info about meter data fields
      that later mapped to physical meter registers
   """
   def __init__(self, fName: str, fUnit: str):
      self.fieldName = fName
      self.fieldUnit = fUnit
      self.fieldMin: float = 0.0
      self.fieldMax: float = 0.0


class meterDataFields(object):

   @staticmethod
   def getMeterDataFieldInfo(fieldName: str) -> [meterDataField, False]:
      arr = [x for x in meterDataFields.data if x.fieldName == fieldName]
      count = len(arr)
      if count == 1:
         return arr[0]
      elif count > 1:
         raise Exception("Duplicate data in meterDataFields table!")
      else:
         return False

   """
      static lookup table to get info about a given meter field by its name
   """
   data: List[meterDataField] = [meterDataField(rn.GridFreqHz, ru.Hz)
      , meterDataField(rn.ModbusAddress, ru.blank)
      , meterDataField(rn.SerialNumber, ru.blank)
      , meterDataField(rn.BaudRate, ru.blank)
      , meterDataField(rn.HardwareVersion, ru.blank)
      , meterDataField(rn.SoftwareVersion, ru.blank)
      , meterDataField(rn.CT_Rate, ru.blank)
      , meterDataField(rn.S0_OutputRate, ru.blank)
      , meterDataField(rn.A3, ru.blank)
      , meterDataField(rn.CycleTime, ru.blank)
      , meterDataField(rn.LineVoltage, ru.Volts)
      , meterDataField(rn.L1_Voltage, ru.Volts)
      , meterDataField(rn.L2_Voltage, ru.Volts)
      , meterDataField(rn.L3_Voltage, ru.Volts)
      , meterDataField(rn.TotalAmps, ru.Amps)
      , meterDataField(rn.L1_Amps, ru.Amps)
      , meterDataField(rn.L2_Amps, ru.Amps)
      , meterDataField(rn.L3_Amps, ru.Amps)
      # active power ~ watts
      , meterDataField(rn.TotalActivePower, ru.ActivePower_kW)
      , meterDataField(rn.L1_ActivePower, ru.ActivePower_kW)
      , meterDataField(rn.L2_ActivePower, ru.ActivePower_kW)
      , meterDataField(rn.L3_ActivePower, ru.ActivePower_kW)
      # reactive power ~ Volt-Ampere reactive i.e. VAR
      , meterDataField(rn.TotalReactivePower, ru.ReactivePower_kVAr)
      , meterDataField(rn.L1_ReactivePower, ru.ReactivePower_kVAr)
      , meterDataField(rn.L2_ReactivePower, ru.ReactivePower_kVAr)
      , meterDataField(rn.L3_ReactivePower, ru.ReactivePower_kVAr)
      , meterDataField(rn.TotalApparentPower, ru.ApparentPower_kVA)
      , meterDataField(rn.L1_ApparentPower, ru.ApparentPower_kVA)
      , meterDataField(rn.L2_ApparentPower, ru.ApparentPower_kVA)
      , meterDataField(rn.L3_ApparentPower, ru.ApparentPower_kVA)
      , meterDataField(rn.TotalPowerFactor, ru.blank)
      , meterDataField(rn.L1_PowerFactor, ru.blank)
      , meterDataField(rn.L2_PowerFactor, ru.blank)
      , meterDataField(rn.L3_PowerFactor, ru.blank)
      , meterDataField(rn.CRC, ru.blank)
      , meterDataField(rn.CombinedCode, ru.blank)
      , meterDataField(rn.TotalActiveEnergy, ru.ActiveEnergy_kWh)
      , meterDataField(rn.L1_TotalActiveEnergy, ru.ActiveEnergy_kWh)
      , meterDataField(rn.L2_TotalActiveEnergy, ru.ActiveEnergy_kWh)
      , meterDataField(rn.L3_TotalActiveEnergy, ru.ActiveEnergy_kWh)
      # reactive energy
      , meterDataField(rn.TotalReactiveEnergy, ru.ReactiveEnergy_kVArh)
      , meterDataField(rn.L1_ReactiveEnergy, ru.ReactiveEnergy_kVArh)
      , meterDataField(rn.L2_ReactiveEnergy, ru.ReactiveEnergy_kVArh)
      , meterDataField(rn.L3_ReactiveEnergy, ru.ReactiveEnergy_kVArh)
      , meterDataField(rn.ForwardActiveEnergy, ru.ActiveEnergy_kWh)
      , meterDataField(rn.L1_ForwardActiveEnergy, ru.ActiveEnergy_kWh)
      , meterDataField(rn.L2_ForwardActiveEnergy, ru.ActiveEnergy_kWh)
      , meterDataField(rn.L3_ForwardActiveEnergy, ru.ActiveEnergy_kWh)]

