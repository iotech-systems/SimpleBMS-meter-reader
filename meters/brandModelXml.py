
import os.path
import xml.etree.ElementTree as et


class brandModelXml(object):

   def __init__(self, brand: str, model: str):
      self.brand = brand
      self.model = model
      self.path = f"brands/{self.brand}/{self.model}.xml"

   def exists(self) -> bool:
      return os.path.exists(self.path)

   def loadXml(self) -> et.ElementTree:
      doc = et.parse(self.path)
      return doc
