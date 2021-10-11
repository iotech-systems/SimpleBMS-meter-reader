
import datetime
import requests as r
import conf.restapi as s
import sbmslib.shared.core.registerNames as rn
import meters.electric.modbusBasedMeter as um
import sbmslib.shared.models.kWhReport as kwr
import sbmslib.shared.models.alarmReport as ar
import sbmslib.shared.models.infoReport as ir


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
            print(f"\ttxt: {res.text}")
         else:
            print(f"none 200 code: {res.status_code}")
      except (r.exceptions.ConnectionError, Exception) as e:
         # unable to connect -> save json to for-later-buffer
         actions.saveForLater(report)
         print(e)

   @staticmethod
   def sendInfo(report: ir.infoReport):
      try:
         print(" --- sending alarm ---")
         url = f"http://{s.SBMS_REST_SERVER}/{s.REST_REPORT_ALARM_URL}"
         jsonBuff = report.toJson()
         res: r.Response = r.put(url, json=jsonBuff)
         print(f"\n\thttp code: {res.status_code}")
         if res.status_code == 200:
            print("\t -> alarm report saved!\n")
            print(f"\ttxt: {res.text}")
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
            print("\t -> alarm report saved!")
            print(f"\t -> res: {res.text}\n")
         else:
            print(f"none 200 code: {res.status_code}")
      except (r.exceptions.ConnectionError, Exception) as e:
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
