
"""
   jobj["streamName"], jobj["streamTable"], jobj["meterBrand"], jobj["meterModel"], \
   jobj["edgeName"], jobj["busType"], jobj["busAddress"],  jobj["dtsUtc"]
"""


class jsonPackageHead(object):

   def __init__(self, jobj):
      self.streamName = jobj["streamName"]
      self.streamTable = jobj["streamTable"]
      self.meterBrand = jobj["meterBrand"]
      self.meterModel = jobj["meterModel"]
      self.edgeName = jobj["edgeName"]
      self.busType = jobj["busType"]
      self.busAddress: int = int(jobj["busAddress"])
      self.dtsUtc = jobj["dtsUtc"]

   def __str__(self) -> str:
      return str(self.__dict__)
