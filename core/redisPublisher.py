import os.path

import redis
import xml.etree.ElementTree as et


class redisConf(object):

   def __init__(self):
      self.__ser: str = ""
      self.__prt: int = 0
      self.__pwd: str = ""
      self.__reads_channel: str = ""
      self.xml = "conf/redis.xml"
      if os.path.exists(self.xml):
         self.conf = et.parse(self.xml).getroot()
      else:
         raise Exception(f"FileNotFound: {self.xml}")

   def server(self) -> str:
      if self.__ser in ["", None]:
         xpath = "arg[@name=\"readsPubServer\"]"
         elm = self.conf.find(xpath)
         tmp = elm.attrib["value"]
         self.__ser = tmp.split(":")[0]
      return self.__ser

   def port(self) -> 0:
      if self.__prt == 0:
         xpath = "arg[@name=\"readsPubServer\"]"
         elm = self.conf.find(xpath)
         tmp = elm.attrib["value"]
         self.__prt = int(tmp.split(":")[1])
      return self.__prt

   def pwd(self) -> str:
      if self.__pwd in ["", None]:
         xpath = "arg[@name=\"readsPubServerPwd\"]"
         elm = self.conf.find(xpath)
         self.__pwd = str(elm.attrib["value"])
      return self.__pwd

   def reads_pub_channel(self) -> str:
      if self.__reads_channel in ["", None]:
         xpath = "arg[@name=\"readsPubChannel\"]"
         elm = self.conf.find(xpath)
         self.__reads_channel = str(elm.attrib["value"])
      return self.__reads_channel

class redisPublisher(object):

   conf: redisConf = None

   def __init__(self):
      if redisPublisher.conf is None:
         redisPublisher.conf = redisConf()
      self.conf = redisPublisher.conf

   def pub_reads(self,  msg: str):
      host = self.conf.server()
      port = self.conf.port()
      pwd: str = self.conf.pwd()
      red = redis.StrictRedis(host, port, password=pwd,
         charset="utf-8", decode_responses=True)
      cnt = red.publish(self.conf.reads_pub_channel(), msg)
      print(cnt)
