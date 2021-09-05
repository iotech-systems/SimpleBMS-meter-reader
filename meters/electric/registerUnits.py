

import enum


class registerUnits(object):

   blank = ""
   ActiveEnergy_kWh = "kWh"
   Amps = "A"
   Volts = "V"
   Hz = "Hz"
   Watts = "W"
   ReactivePower_kVAr = "kVAr"
   ApparentPower_kVA = "kVA"
   ActivePower_W = "W"
   ActivePower_kW = "kW"
   ReactiveEnergy_kVArh = "kVArh"


class registerMeasureUnits(enum.Enum):

   noUnit = 0
   # basics
   Hz = enum.auto()
   Amps = enum.auto()
   Volts = enum.auto()
   # computed
   ActivePower_W = enum.auto()
   ActivePower_kW = enum.auto()
   ActiveEnergy_Wh = enum.auto()
   ActiveEnergy_kWh = enum.auto()
   ApparentPower_VA = enum.auto()
   ApparentPower_kVA = enum.auto()
   ReactivePower_VAr = enum.auto()
   ReactivePower_kVAr = enum.auto()
   ReactiveEnergy_VArh = enum.auto()
   ReactiveEnergy_kVArh = enum.auto()
