
import json
import datetime as dt
from sbmslib.shared.utils.jsonx import jsonx


DATE_FORMAT = "%Y-%m-%d %H:%M:%S UTC"


class coreModel(object):

   def __init__(self):
      self.meterDBID: int = 0
      self.className = self.__class__.__name__
      self.dtsUTC = dt.datetime.utcnow().strftime(DATE_FORMAT)

   def setMeterDBID(self, meterDBID: int):
      self.meterDBID = meterDBID

   def set(self, **kwargs):
      pass

   def toJson(self):
      return json.dumps(self, default=lambda o: o.__dict__)

   def fromJson(self, jsonBuff: str):
      # set core fields
      jObj = jsonx.getJsonObj(jsonBuff)
      if self.className != jObj["className"]:
         raise Exception(f"bad className : {self.className}")
      self.meterDBID: int = int(jObj["meterDBID"])
      self.dtsUTC: str = str(jObj["dtsUTC"])
      # return for child fields
      return jObj

   @classmethod
   def __json_obj__(cls, jsonBuff: str):
      return jsonx.getJsonObj(jsonBuff)
