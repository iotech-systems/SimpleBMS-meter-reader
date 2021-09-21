
"""
CREATE TABLE streams.basic_pwr_stats (
   fk_meter_dbid int4 NOT NULL,
   reading_dts_utc timestamp NOT NULL,
   grid_freq_hz numeric(4, 2) NULL,
   line_volts numeric(6, 2) NULL,
   l1_volts numeric(6, 2) NULL,
   l2_volts numeric(6, 2) NULL,
   l3_volts numeric(6, 2) NULL,
   total_amps numeric(6, 2) NULL,
   l1_amps numeric(6, 2) NULL,
   l2_amps numeric(6, 2) NULL,
   l3_amps numeric(6, 2) NULL,
   total_active_pwr numeric(8, 2) NULL,
   l1_active_pwr numeric(8, 2) NULL,
   l2_active_pwr numeric(8, 2) NULL,
   l3_active_pwr numeric(8, 2) NULL,
   total_reactive_pwr numeric(8, 2) NULL,
   l1_reactive_pwr numeric(8, 2) NULL,
   l2_reactive_pwr numeric(8, 2) NULL,
   l3_reactive_pwr numeric(8, 2) NULL,
   row_ins_dts_utc timestamp NOT NULL DEFAULT now()
);
"""

from sbmslib.shared.models import coreModel


class basicPwrStatsReport(coreModel.coreModel):

   def __init__(self):
      super(basicPwrStatsReport, self).__init__()
      self.grid_freq_hz: float = 0.0
      # - - - - - - - - -
      self.line_volts: float = 0.0
      self.l1_volts: float = 0.0
      self.l2_volts: float = 0.0
      self.l3_volts: float = 0.0
      # - - - - - - - - -
      self.total_amps: float = 0.0
      self.l1_amps: float = 0.0
      self.l2_amps: float = 0.0
      self.l3_amps: float = 0.0
      # - - - - - - - - -
      self.total_active_pwr: float = 0.0
      self.l1_active_pwr: float = 0.0
      self.l2_active_pwr: float = 0.0
      self.l3_active_pwr: float = 0.0
      # - - - - - - - - -
      self.total_reactive_pwr: float = 0.0
      self.l1_reactive_pwr: float = 0.0
      self.l2_reactive_pwr: float = 0.0
      self.l3_reactive_pwr: float = 0.0
      # - - - - - - - - -
      self.row_ins_dts_utc: str = "default"

   def setMeterDBID(self, meterDBID: int):
      self.meterDBID = meterDBID

   def set(self, grid_freq_hz: float = 0.0, line_volts: float = 0.0, l1_volts: float = 0.0
           , l2_volts: float = 0.0, l3_volts: float = 0.0, total_amps: float = 0.0, l1_amps: float = 0.0
           , l2_amps: float = 0.0, l3_amps: float = 0.0, total_active_pwr: float = 0.0, l1_active_pwr: float = 0.0
           , l2_active_pwr: float = 0.0, l3_active_pwr: float = 0.0, total_reactive_pwr: float = 0.0
           , l1_reactive_pwr: float = 0.0, l2_reactive_pwr: float = 0.0, l3_reactive_pwr: float = 0.0):
      # - - - - - -
      self.grid_freq_hz = grid_freq_hz
      self.line_volts = line_volts
      self.l1_volts = l1_volts
      self.l2_volts = l2_volts
      self.l3_volts = l3_volts
      self.total_amps = total_amps
      self.l1_amps = l1_amps
      self.l2_amps = l2_amps
      self.l3_amps = l3_amps
      self.total_active_pwr = total_active_pwr
      self.l1_active_pwr = l1_active_pwr
      self.l2_active_pwr = l2_active_pwr
      self.l3_active_pwr = l3_active_pwr
      self.total_reactive_pwr = total_reactive_pwr
      self.l1_reactive_pwr = l1_reactive_pwr
      self.l2_reactive_pwr = l2_reactive_pwr
      self.l3_reactive_pwr = l3_reactive_pwr

   def fromJson(self, jsonBuff: str):
      # sets super fields: meterDBID; dtsUTC;
      jObj = super(basicPwrStatsReport, self).fromJson(jsonBuff)
      self.grid_freq_hz = float(jObj["grid_freq_hz"])
      self.line_volts = float(jObj["line_volts"])
      self.l1_volts = float(jObj["l1_volts"])
      self.l2_volts = float(jObj["l2_volts"])
      self.l3_volts = float(jObj["l3_volts"])
      self.total_amps = float(jObj["total_amps"])
      self.l1_amps = float(jObj["l1_amps"])
      self.l2_amps = float(jObj["l2_amps"])
      self.l3_amps = float(jObj["l3_amps"])
      self.total_active_pwr = float(jObj["total_active_pwr"])
      self.l1_active_pwr = float(jObj["l1_active_pwr"])
      self.l2_active_pwr = float(jObj["l2_active_pwr"])
      self.l3_active_pwr = float(jObj["l3_active_pwr"])
      self.total_reactive_pwr = float(jObj["total_reactive_pwr"])
      self.l1_reactive_pwr = float(jObj["l1_reactive_pwr"])
      self.l2_reactive_pwr = float(jObj["l2_reactive_pwr"])
      self.l3_reactive_pwr = float(jObj["l3_reactive_pwr"])
