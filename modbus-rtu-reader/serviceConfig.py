

import data.models.dbMeterInfo as dbmi

"""
   this should get loaded from config database
"""


class serviceConfig(object):

   scanIntervalMinutes = 6
   sbmsGateIP = "192.168.40.106"
   ttyPorts = ("/dev/ttyUSB2", "/dev/ttyUSB1")

   """ m0 = (1, "orno504")
   m1 = (2, "orno516")
   m2 = (4, "orno516") """

   devStr = ""
   m0: dbmi.dbMeterInfo = dbmi.dbMeterInfo(1, 1001, "", "orno504")
   m1: dbmi.dbMeterInfo = dbmi.dbMeterInfo(2, 1003, "", "orno516")
   m2: dbmi.dbMeterInfo = dbmi.dbMeterInfo(4, 1005, "", "orno516")

   meters = {
         "/dev/ttyUSB0": (m0, m1, m2),
         "/dev/ttyUSBx": None
      }

   @staticmethod
   def dump():
      print(f"\nttyPorts: {serviceConfig.ttyPorts}\n")
      print(f"meters: {serviceConfig.meters}")
