

# <job type="registerStream" startIndex="1"  streamType="kWhrs" intervalMins="4" />
class jobXmlAttrib(object):

   lastRunStartDTS = "lastRunStartDTS"
   lastRunEndDTS = "lastRunEndDTS"
   intervalMins = "intervalMins"
   streamType = "streamType"
   type = "type"
   startIndex = "startIndex"


# <meter busAddress="1" brand="orno" modelXML="orno504.xml" />
class meterXmlAttrib(object):

   busAddress = "busAddress"
   brand = "brand"
   modelXML = "modelXML"


class modbusAttrib(object):

   start = "start"


class xmlConsts(object):

   unknown = "?"


class dtsFormats(object):

   std = "%Y-%m-%d %H:%M:%S"
