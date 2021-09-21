
from typing import List

"""
total: kWhReading.kWhReading = \
         [x for x in lst if x.regName == rn.TotalActiveEnergy][0]
      l1: kWhReading.kWhReading = \
         [x for x in lst if x.regName == rn.L1_TotalActiveEnergy][0]
      l2: kWhReading.kWhReading = \
         [x for x in lst if x.regName == rn.L2_TotalActiveEnergy][0]
      l3: kWhReading.kWhReading = \
         [x for x in lst if x.regName == rn.L3_TotalActiveEnergy][0]
"""


class kWhReading(object):

   def __init__(self, jobj):
      self.regName: str = jobj["regName"]
      self.regVal: object = jobj["regVal"]
      self.regValUnit: str = jobj["regValUnit"]
      self.fldRegMapped: bool = bool(jobj["fldRegMapped"])
      self.hasError: bool = bool(jobj["hasError"])
      self.formatter: str = jobj["formatter"]

   @staticmethod
   def getRegValueFromName(regName: str, regList: []):
      regVal = next((r for r in regList if r.regName == regName), None)
      return regVal
