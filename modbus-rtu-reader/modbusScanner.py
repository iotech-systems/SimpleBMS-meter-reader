
import time
import setproctitle
import meters.electric.universalMeter as um
import core.system as sys
import data.models.dbMeterInfo as dbmi
import data.models.alarmReport as ar
import serviceConfig as sc
import core.consts as consts


class modbusScanner(object):

   def __init__(self, serPort: str, meters: tuple):
      """
      c-tor
      """
      print(f"\n[c-tor: portReader; {serPort}; {meters}; ]\n")
      self.serPort = serPort
      self.meters: tuple = meters
      self.scanDelaySecs = sc.serviceConfig.scanIntervalMinutes * 60
      self.errorDelaySecs = 60.0
      tty = self.serPort.replace("/dev/", "")
      self.procName = f"iot-scr:{tty}"

   def loadConfig(self) -> bool:
      """
      :return:
      """
      return True

   def run(self):
      """
      :rtype: bool
      """
      # set process title
      setproctitle.setproctitle(self.procName)
      while True:
         try:
            for meter in self.meters:
               self.__on_each_meter(meter)
            # delay on port scan
            print("\n\t+ + + main bus scan delay + + +\n")
            time.sleep(self.scanDelaySecs)
         except Exception as e:
            print(e)
            time.sleep(1.0)

   def __on_each_meter(self, m: dbmi.dbMeterInfo):
      try:
         print(f"\n\n [ >> meter: {m} << ]\n")
         # - - - - - -
         if m is None:
            print("\n\t * * * meter is None * * *")
            return
         # - - - - - -
         uniMeter: um.universalMeter = um.universalMeter("", self.serPort, meterInfo=m)
         # test modbus id
         if not uniMeter.ping():
            print(f"Meter @modbusID: {m.modbusID} not responding!")
         time.sleep(1.0)
         if not uniMeter.ping():
            print(f"Meter @modbusID: {m.modbusID} not responding!")
            report = ar.alarmReport(uniMeter.meterInfo.dbID,
               consts.errorLevels.error, "DeadPing", "NoPongDetected")
            sys.system.sendAlarm(report)
            return
         # meter found
         print(f"\t > Meter ping @modbusID: {m.modbusID} ~ Ok")
         uniMeter.readRegisters()
         uniMeter.close()
         # save scan results
         if len(uniMeter.registersOut):
            sys.system.sendData_kwhrs(uniMeter)
         # - - - -
      except Exception as e:
         print(e)
