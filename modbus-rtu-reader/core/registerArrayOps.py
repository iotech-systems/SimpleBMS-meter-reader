
import meters.electric.register as r


class registerArrayOps(object):

   def __init__(self, arr: []):
      self.regArr: [] = arr

   def findByName(self, regName: str) -> [r.register, None]:
      for item in self.regArr:
         reg: r.register = item
         if reg.name == regName:
            return reg
      # - - reg not found ---
      return None
