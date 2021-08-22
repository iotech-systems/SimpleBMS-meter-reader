
import meters.core


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class orno504(meters.core.SETTINGS):

   def __init__(self):
      super(orno504, self).__init__()
      self.parity = meters.core.PARITY.none
      self.baudrate = meters.core.BAUDRATES.br_09600
      self.timeout = 0.10


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class orno516(meters.core.SETTINGS):

   def __init__(self):
      super(orno516, self).__init__()
      self.parity = meters.core.PARITY.even
      self.baudrate = meters.core.BAUDRATES.br_09600
      self.timeout = 0.25
