
from sbmslib.shared.models import coreModel


class alarmReport(coreModel.coreModel):

   def __init__(self):
      super(alarmReport, self).__init__()
      self.meterDBID: int = 0
      self.level: str = ""
      self.alarm_tag: str = ""
      self.alarm_msg: str = ""

   def setMeterDBID(self, meterDBID: int):
      super(alarmReport, self).setMeterDBID(meterDBID)

   def set(self, meterDBID: int, level: str, alarmTag: str, alarmMsg: str):
      super(alarmReport, self).setMeterDBID(meterDBID)
      self.level: str = level
      self.alarm_tag = alarmTag
      self.alarm_msg = alarmMsg

   def fromJson(self, jsonBuff: str):
      jObj = alarmReport.__json_obj__(jsonBuff)
      if self.className != jObj["className"]:
         raise Exception(f"bad _type_ : {self.className}")
      self.meterDBID: int = int(jObj["meterDBID"])
      self.dtsUTC: str = str(jObj["dtsUTC"])
      self.level: str = str(jObj["level"])
      self.alarm_tag: str = str(jObj["alarm_tag"])
      self.alarm_msg: str = str(jObj["alarm_msg"])
