
import minimalmodbus as mm
from .xcmd import xcmd


class readReg(xcmd):

   def __init__(self):
      super(readReg, self).__init__()
      self.info = "\n\tRead register command: "
      self.modbusID: int = 0
      self.address: int = 0
      self.parsedArgs: {} = {}

   def setArgs(self, args: []):
      self.args = args

   def run(self):
      self.parse()
      super(readReg, self).run()

   def parse(self):
      argName: str = ""
      for a in self.args:
         if a.startswith("-"):
            argName = a
         # self.parsedArgs[argName]
