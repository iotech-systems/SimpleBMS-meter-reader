
"""
package = {"streamName": streamName, "streamTable": streamTable
         , "edgeName": sysutils.hostName(), "modbusAddress": busAdr
         , "dtsUTC": datetime.datetime.utcnow().strftime(dtsFormats.std)
         , "readings": readings}
"""

from typing import List
from datetime import datetime
from core.sys import dtsFormats
from sbmslib.shared.utils.sysutils import sysutils


class jsonPackageMaker(object):

   def __init__(self):
      self.dtsUtc = datetime.utcnow()
      self.edgeName = sysutils.hostName()
      self.busType = "modbus"

   def make(self, streamName: str, streamTable: str, meterBrand: str
         , meterModel: str, modbusAddress: int, readTime: float, readings: List[dict]):
      # - - - - - - - - - - - -
      return {"streamName": streamName, "streamTable": streamTable
         , "meterBrand": meterBrand, "meterModel": meterModel, "readTimeSecs": readTime 
         , "edgeName": self.edgeName, "busType": self.busType, "busAddress": modbusAddress
         , "dtsUtc": self.dtsUtc.strftime(dtsFormats.std), "readings": readings}

