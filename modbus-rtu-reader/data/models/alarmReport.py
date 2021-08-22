
import json
import data.models.coreModel as cm


class alarmReport(cm.coreModel):

   def __init__(self, meterDBID: int, level: str, alarmTag: str, alarmMsg: str):
      super(alarmReport, self).__init__(meterDBID, "alarmReport")
      self.meterDBID: int = meterDBID
      self.level: str = level
      self.alarm_tag = alarmTag
      self.alarm_msg = alarmMsg

   def toJson(self):
      return json.dumps(self, default=lambda o: o.__dict__)
