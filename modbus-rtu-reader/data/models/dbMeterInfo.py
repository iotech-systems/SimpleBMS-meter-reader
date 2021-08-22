

class dbMeterInfo(object):

   def __init__(self, modbusid: int,  dbid: int, devStr: str, meterTag: str):
      self.modbusID = modbusid
      self.dbID: int = dbid
      self.devStr = devStr
      self.meterTag = meterTag
