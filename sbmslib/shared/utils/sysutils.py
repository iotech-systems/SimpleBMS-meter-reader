
from typing import List
from sbmslib.shared.models.kWhReading import kWhReading


class sysutils(object):

   @classmethod
   def hostName(cls) -> str:
      with open("/etc/hostname", "r") as file:
         buff: str = file.read()
      return buff.strip()

   @classmethod
   def findRegister(cls, regList: List[kWhReading], regName: str) -> [kWhReading, None]:
      regVal = next((r for r in regList if r.regName == regName), None)
      return regVal
