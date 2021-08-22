
import meters.core as c
import brands.orno.registers as r
import brands.orno.settings as oc


class meterLoader(object):

   @staticmethod
   def loadRegisters(meterTag: str) -> tuple:
      opts = {"orno504": r.REGS_504,
         "orno516": r.REGS_516}
      regs = opts[meterTag]
      return regs

   @staticmethod
   def loadSettings(meterTag: str) -> c.SETTINGS:
      opts = {"orno504": oc.orno504(),
              "orno516": oc.orno516()}
      obj = opts[meterTag]
      return obj
