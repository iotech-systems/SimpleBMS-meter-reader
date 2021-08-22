
import meters.electric.readingFixer as rf


class dataMode:

   rawRegister = "register"
   numFloat = "float"
   numInt = "int"
   strString = "string"


class register(object):

   def __init__(self, name: str = "", adr: int = 0, size: int = 0
         , mode: str = dataMode.rawRegister, decpnt: int = 0
         , unit: str = "", enable: bool = True, fixer=None, fixerArgs=None):
      # - - - - - - - - - - - - - - - - -
      self.name: str = name
      self.address: int = adr
      self.size: int = size
      self.decpnt: int = decpnt
      self.mode: str = mode
      self.unit: str = unit
      self.enable: bool = enable
      self.regValue: object = None
      self.fixer = fixer
      self.fixerArgs = fixerArgs

   def setRegValue(self, val):
      self.regValue = val

   def print(self):
      if self.fixer is not None:
         # print(f"raw regValue: {self.regValue}")
         self.regValue = self.fixer(self.regValue)
      # - - - -
      print(f"\n -> name: {self.name}; address: {self.address}; size: {self.size}; mode: {self.mode};"
         f"\n -> decpnt: {self.decpnt}; unit: {self.unit}; enable: {self.enable}; regValue: {self.regValue};\n")
