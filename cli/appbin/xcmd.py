

class xcmd(object):

   def __init__(self):
      self.args: [] = None
      self.info: str = ""

   def setArgs(self, args):
      self.args = args

   def run(self):
      print(self.info)

   def parse(self):
      pass
