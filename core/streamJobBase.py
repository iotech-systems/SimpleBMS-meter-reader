
import xml.etree.ElementTree as xmlTree


class streamJobBase(object):

   def __init__(self, xmlJob: xmlTree.Element):
      print("[ c-tor: streamJobBase ]")
      self.xmlJob = xmlJob
      self.initObj = None
      self.errorCount: int = 0
      self.returnCode: int = 0

   def run(self, **kwargs) -> bool:
      pass
