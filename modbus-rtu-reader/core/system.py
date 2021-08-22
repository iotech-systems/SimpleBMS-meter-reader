
import requests as r
import core.settings as s
import core.registerArrayOps as rao
import meters.electric.registerNames as rn
import meters.electric.universalMeter as um
import data.models.kWhReport as kwr
import data.models.alarmReport as ar


class system(object):

   def __init__(self):
      pass

   @staticmethod
   def sendAlarm(report: ar.alarmReport):
      print(" --- sending alarm ---")
      url = f"http://{s.SBMS_REST_SERVER}/{s.REST_REPORT_ALARM_URL}"
      jsonBuff = report.toJson()
      res: r.Response = r.put(url, json=jsonBuff)
      print(f"\n\thttp code: {res.status_code}")
      if res.status_code == 200:
         print("\t -> alarm report saved!\n")
      else:
         pass

   @staticmethod
   def sendData_kwhrs(m: um.universalMeter):
      print(" --- sending kwhrs ---")
      regOps: rao.registerArrayOps = rao.registerArrayOps(m.registersOut)
      regTotalEng = regOps.findByName(rn.regsNames.ActiveEnergy)
      regL1Eng = regOps.findByName(rn.regsNames.L1_TotalActiveEnergy)
      regL2Eng = regOps.findByName(rn.regsNames.L2_TotalActiveEnergy)
      regL3Eng = regOps.findByName(rn.regsNames.L3_TotalActiveEnergy)
      # - - - -
      total: float = float(str(regTotalEng.regValue))
      l1: float = 0.0
      if regL1Eng is not None:
         l1 = float(str(regL1Eng.regValue))
      l2: float = 0.0
      if regL2Eng is not None:
         l2 = float(str(regL2Eng.regValue))
      l3: float = 0.0
      if regL3Eng is not None:
         l3 = float(str(regL3Eng.regValue))
      # - - - -
      data: kwr.kWhReport = kwr.kWhReport(m.meterInfo.dbID, total, l1, l2, l3)
      jsonBuff = data.toJson()
      url = f"http://{s.SBMS_REST_SERVER}/{s.REST_REPORT_KWH_URL}"
      res: r.Response = r.put(url, json=jsonBuff)
      print(f"\n\thttp code: {res.status_code}")
      if res.status_code == 200:
         print("\t -> hwh report saved!\n")
      else:
         pass
