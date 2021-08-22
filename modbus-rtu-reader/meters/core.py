
STOPBITS: int = 2


class BAUDRATES(object):

   br_02400: int = 2400
   br_04800: int = 4800
   br_09600: int = 9600
   br_19200: int = 19200


class PARITY(object):

   even: str = "E"
   none: str = "N"
   odd: str = "O"


class SETTINGS(object):

   def __init__(self):
      self.baudrate: int = BAUDRATES.br_09600
      self.parity: str = PARITY.none
      self.stopbits: int = 1
      self.timeout: float = 0.1

   def print(self):
      print(f"parity: {self.parity}; baudrate: {self.baudrate}; stopbits: {self.stopbits};")
