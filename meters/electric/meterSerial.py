
import meters.core
import xml.etree.ElementTree as et


# <serial baudrate="9600" parity="N" stopbits="1" timeoutSecs="0.15" />
class meterSerial(object):

   def __init__(self, serialXml: et.Element):
      print("[ c-tor: meterSerial ]")
      self.serialXml = serialXml
      # print(self.serialXml.attrib)
      self.parity: str = self.serialXml.attrib["parity"]
      self.baudrate: int = int(self.serialXml.attrib["baudrate"])
      self.stopbits: int = int(self.serialXml.attrib["stopbits"])
      self.timeout: float = float(self.serialXml.attrib["timeoutSecs"])
