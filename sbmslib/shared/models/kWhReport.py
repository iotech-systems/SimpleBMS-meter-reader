
from sbmslib.shared.models import coreModel


class kWhReport(coreModel.coreModel):

   def __init__(self):
      super(kWhReport, self).__init__()
      self.meterDBID: int = 0
      self.total: float = 0.0
      self.l1: float = 0.0
      self.l2: float = 0.0
      self.l3: float = 0.0

   def setMeterDBID(self, meterDBID: int):
      super(kWhReport, self).setMeterDBID(meterDBID)

   def set(self, meterDBID: int, total: float, l1: float, l2: float, l3: float):
      super(kWhReport, self).setMeterDBID(meterDBID)
      self.total: float = total
      self.l1: float = l1
      self.l2: float = l2
      self.l3: float = l3

   def fromJson(self, jsonBuff: str):
      jObj = kWhReport.__json_obj__(jsonBuff)
      if self.className != jObj["className"]:
         raise Exception(f"bad className : {self.className}")
      self.meterDBID: int = int(jObj["meterDBID"])
      self.dtsUTC: str = str(jObj["dtsUTC"])
      self.total: float = float(jObj["total"])
      self.l1: float = float(jObj["l1"])
      self.l2: float = float(jObj["l2"])
      self.l3: float = float(jObj["l3"])
