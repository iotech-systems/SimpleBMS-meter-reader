
import datetime
import requests as r
import conf.restapi as s
import sbmslib.shared.core.registerNames as rn
import meters.electric.modbusBasedMeter as um
import sbmslib.shared.models.kWhReport as kwr
import sbmslib.shared.models.alarmReport as ar


BASE_DATE_2020 = datetime.datetime(2020, 1, 1, 0, 0, 1)


class actions(object):

   def __init__(self):
      pass

   @staticmethod
   def sendAlarm(report: ar.alarmReport):
      try:
         print(" --- sending alarm ---")
         url = f"http://{s.SBMS_REST_SERVER}/{s.REST_REPORT_ALARM_URL}"
         jsonBuff = report.toJson()
         res: r.Response = r.put(url, json=jsonBuff)
         print(f"\n\thttp code: {res.status_code}")
         if res.status_code == 200:
            print("\t -> alarm report saved!\n")
         else:
            print(f"none 200 code: {res.status_code}")
      except (r.exceptions.ConnectionError, Exception) as e:
         # unable to connect -> save json to for-later-buffer
         actions.saveForLater(report)
         print(e)

   @staticmethod
   def send2streamer(jsonPackage: str):
      try:
         print(" --- sending alarm ---")
         url = f"http://{s.SBMS_REST_SERVER}/{s.REST_REPORT_STREAMER}"
         res: r.Response = r.put(url, json=jsonPackage)
         print(f"\n\thttp code: {res.status_code}")
         if res.status_code == 200:
            print("\t -> alarm report saved!\n")
         else:
            print(f"none 200 code: {res.status_code}")
      except (r.exceptions.ConnectionError, Exception) as e:
         # unable to connect -> save json to for-later-buffer
         print(e)

   @staticmethod
   def sendData_kwhrs(m: um.modbusBasedMeter):
      report = None
      try:
         print(" --- sending kwhrs ---")
         regOps: rao.registerArrayOps = rao.registerArrayOps(m.registersOut)
         regTotalEng = regOps.findByName(rn.registerNames.TotalActiveEnergy)
         regL1Eng = regOps.findByName(rn.registerNames.L1_TotalActiveEnergy)
         regL2Eng = regOps.findByName(rn.registerNames.L2_TotalActiveEnergy)
         regL3Eng = regOps.findByName(rn.registerNames.L3_TotalActiveEnergy)
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
         report: kwr.kWhReport = kwr.kWhReport()
         report.set(m.meterInfo.meterDBID, total, l1, l2, l3)
         url = f"http://{s.SBMS_REST_SERVER}/{s.REST_REPORT_KWH_URL}"
         res: r.Response = r.put(url, json=report.toJson())
         print(f"\n\thttp code: {res.status_code}")
         if res.status_code == 200:
            print("\t -> hwh report saved!\n")
         else:
            pass
      except (r.exceptions.ConnectionError, Exception) as e:
         actions.saveForLater(report)
         print(e)

   @staticmethod
   def saveForLater(report: [ar.alarmReport, kwr.kWhReport]):
      try:
         clsName: str = report.__class__.__name__
         print(f"safe for later: {clsName}")
         diff = (datetime.datetime.utcnow() - BASE_DATE_2020)
         fn = f"{clsName}_{int(diff.total_seconds())}.json"
         with open(f"data/cache/{fn}", "w") as file:
            file.writelines(report.toJson())
      except:
         # just let it die for now
         pass
