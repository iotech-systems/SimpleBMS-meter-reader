

class MeterInfo(object):

   def __init__(self, address: int
                , dbid: int, devStr: str
                , mBrand: str, mModel: str):
      # - - - - - - - - - -
      self.modbusAddress: int = address
      self.meterDBID: int = dbid
      self.deviceSystemString: str = devStr
      self.meterBrand: str = mBrand
      self.meterModel: str = mModel
