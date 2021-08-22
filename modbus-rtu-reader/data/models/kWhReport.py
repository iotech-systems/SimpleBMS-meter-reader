
import json
import data.models.coreModel as cm


class kWhReport(cm.coreModel):

   def __init__(self, meterDBID: int, total: float, l1: float, l2: float, l3: float):
      super(kWhReport, self).__init__(meterDBID, "kWhReport")
      self.meterDBID: int = meterDBID
      self.total: float = total
      self.l1: float = l1
      self.l2: float = l2
      self.l3: float = l3

   def toJson(self):
      return json.dumps(self, default=lambda o: o.__dict__)
