
import xml.etree.ElementTree as et
from meters.electric.registerFormatter import registerFormatter as formatter


# <register address="0x0016" size="2" name="L3_TotalActiveEnergy" decpnt="2" mode="float" unit="Amps" />
class register(object):

   def __init__(self, xmlReg: et.Element):
      # - - - - - - - - - - - - - - - - -
      self.xmlReg = xmlReg
      self.name: str = self.xmlReg.attrib["name"]
      hexString = self.xmlReg.attrib["address"]
      self.address: int = int(hexString, 16)
      self.size: int = int(self.xmlReg.attrib["size"])
      self.decpnt: int = int(self.xmlReg.attrib["decpnt"])
      # -- register if missing or set to "" in xml --
      self.mode: str = "register"
      if "mode" in self.xmlReg.attrib.keys() and self.xmlReg.attrib["mode"] != "":
         self.mode: str = self.xmlReg.attrib["mode"]
      # - - -
      self.unit: str = self.xmlReg.attrib["unit"]
      self.regValue: object = None
      self.formatFuncName = None
      if "formatter" in self.xmlReg.attrib.keys():
         self.formatFuncName = self.xmlReg.attrib["formatter"]

   def setRegValue(self, val):
      if self.formatFuncName is not None:
         func = getattr(formatter, self.formatFuncName)
         self.regValue = func(val)
      else:
         self.regValue = val

   def print(self, printSkinny: bool = True):
      if printSkinny:
         print(f"\n\t\t *** {self.name}: {self.regValue} {self.unit} ***\n")
      else:
         print(f"\n\t -> name: {self.name}; registerAddress: {self.address}; size: {self.size}; mode: {self.mode};"
            f"\n\t -> decpnt: {self.decpnt}; unit: {self.unit}; regValue: {self.regValue};"
               f"\n\t\t *** {self.name}: {self.regValue} {self.unit} ***\n")
