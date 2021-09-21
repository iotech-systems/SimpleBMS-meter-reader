
# register names table
class registerNames(object):

   # single phase names & total reads for 3 phase meters
   GridFreqHz = "GridFreqHz"
   ModbusAddress = "ModbusAddress"
   SerialNumber = "SerialNumber"
   # ReactiveEnergy = "ReactiveEnergy"
   BaudRate = "BaudRate"
   HardwareVersion = "HardwareVersion"
   SoftwareVersion = "SoftwareVersion"
   CT_Rate = "CT_Rate"
   S0_OutputRate = "S0_OutputRate"
   A3 = "A3"
   CycleTime = "CycleTime"
   # voltage ~ V
   LineVoltage = "LineVoltage"                              # used by 1phase and 3phase meters
   L1_Voltage = "L1_Voltage"
   L2_Voltage = "L2_Voltage"
   L3_Voltage = "L3_Voltage"
   # amps ~ A
   TotalAmps = "TotalAmps"                                  # used by 1phase and 3phase meters
   L1_Amps = "L1_Amps"
   L2_Amps = "L2_Amps"
   L3_Amps = "L3_Amps"
   # active power ~ watts
   TotalActivePower = "TotalActivePower"                    # used by 1phase and 3phase meters
   L1_ActivePower = "L1_ActivePower"
   L2_ActivePower = "L2_ActivePower"
   L3_ActivePower = "L3_ActivePower"
   # reactive power ~ Volt-Ampere reactive i.e. VAR
   TotalReactivePower = "TotalReactivePower"                # used by 1phase and 3phase meters
   L1_ReactivePower = "L1_ReactivePower"
   L2_ReactivePower = "L2_ReactivePower"
   L3_ReactivePower = "L3_ReactivePower"
   # apparent power ~ units of Volt-amp (VA)
   TotalApparentPower = "TotalApparentPower"                # used by 1phase and 3phase meters
   L1_ApparentPower = "L1_ApparentPower"
   L2_ApparentPower = "L2_ApparentPower"
   L3_ApparentPower = "L3_ApparentPower"
   # power factor
   TotalPowerFactor = "TotalPowerFactor"                    # used by 1phase and 3phase meters
   L1_PowerFactor = "L1_PowerFactor"
   L2_PowerFactor = "L2_PowerFactor"
   L3_PowerFactor = "L3_PowerFactor"
   # misc
   CRC = "CRC"
   CombinedCode = "CombinedCode"
   # kwh ~ kWh
   TotalActiveEnergy = "TotalActiveEnergy"                  # used by 1phase and 3phase meters
   L1_TotalActiveEnergy = "L1_TotalActiveEnergy"
   L2_TotalActiveEnergy = "L2_TotalActiveEnergy"
   L3_TotalActiveEnergy = "L3_TotalActiveEnergy"
   # - - - -
   TotalReactiveEnergy = "TotalReactiveEnergy"              # used by 1phase and 3phase meters
   L1_ReactiveEnergy = "L1_ReactiveEnergy"
   L2_ReactiveEnergy = "L2_ReactiveEnergy"
   L3_ReactiveEnergy = "L3_ReactiveEnergy"
   # forward active energy
   ForwardActiveEnergy = "ForwardActiveEnergy"
   L1_ForwardActiveEnergy = "L1_ForwardActiveEnergy"
   L2_ForwardActiveEnergy = "L2_ForwardActiveEnergy"
   L3_ForwardActiveEnergy = "L3_ForwardActiveEnergy"
