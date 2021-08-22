
import meters.electric.register as r
import meters.electric.registerNames as rn
import meters.electric.readingFixer as rf
import meters.electric.registerUnits as ru


REGS_504 = (
   r.register(name=rn.regsNames.Voltage, adr=0x00, size=1, decpnt=1,
               unit=ru.registerUnits.Volts, enable=True),
   r.register(name=rn.regsNames.Current, adr=0x01, size=1, decpnt=1,
               unit=ru.registerUnits.Amps, enable=True),
   r.register(name=rn.regsNames.Frequency, adr=0x02, size=1, decpnt=1,
               unit=ru.registerUnits.Hz, enable=True),
   r.register(name=rn.regsNames.ActivePower, adr=0x03, size=1, decpnt=0,
               unit=ru.registerUnits.Watts, enable=True),
   r.register(name=rn.regsNames.ReactivePower, adr=0x04, size=1, decpnt=1,
               unit="Var", enable=False),
   r.register(name=rn.regsNames.ApparentPower, adr=0x05, size=1, decpnt=0,
               unit="VA", enable=False),
   r.register(name=rn.regsNames.PowerFactor, adr=0x06, size=1, decpnt=3,
               unit=ru.registerUnits.noUnit, enable=True),
   # adam said it should be divided by 1000
   r.register(name=rn.regsNames.ActiveEnergy, adr=0x07, size=2, decpnt=0,
               mode=r.dataMode.numInt, unit=ru.registerUnits.kWh,
               fixer=rf.readingFixer.divide1000r2, enable=True),
   # - - - -
   r.register(name=rn.regsNames.ReactiveEnergy, adr=0x09, size=2, decpnt=1,
               unit="Varh", enable=False),
   r.register(name=rn.regsNames.SerialNumber, adr=0x0B, size=3, decpnt=0,
               unit=ru.registerUnits.noUnit, enable=False),
   r.register(name=rn.regsNames.BaudRate, adr=0x0E, size=1, decpnt=0,
               unit=ru.registerUnits.noUnit, enable=True),
   r.register(name=rn.regsNames.ModbusAddress, adr=0x0F, size=1, decpnt=0,
               unit=ru.registerUnits.noUnit, enable=True)
   )


REGS_516 = (
   r.register(name=rn.regsNames.SerialNumber, adr=0x00, size=2, decpnt=0,
               mode=r.dataMode.numInt, unit=ru.registerUnits.noUnit, enable=True),
   r.register(name=rn.regsNames.ModbusAddress, adr=0x02, size=1, decpnt=0,
               mode=r.dataMode.rawRegister, unit=ru.registerUnits.noUnit, enable=True),
   r.register(name=rn.regsNames.Frequency, adr=0x14, size=2, decpnt=1,
               mode=r.dataMode.numFloat, unit=ru.registerUnits.Hz,
               fixer=rf.readingFixer.round2, enable=True),
   r.register(name=rn.regsNames.SoftwareVersion, adr=0x04, size=2, decpnt=3,
               mode=r.dataMode.numFloat, unit=ru.registerUnits.noUnit,
               fixer=rf.readingFixer.round2, enable=True),
   r.register(name=rn.regsNames.HardwareVersion, adr=0x06, size=2, decpnt=3,
               mode=r.dataMode.numFloat, unit=ru.registerUnits.noUnit, enable=True),
   # - - - read kWh ~ active energy - - -
   r.register(name=rn.regsNames.ActiveEnergy, adr=0x100, size=2, decpnt=0,
               mode=r.dataMode.numFloat, unit=ru.registerUnits.kWh,
               fixer=rf.readingFixer.round2, enable=True),
   r.register(name=rn.regsNames.L1_TotalActiveEnergy, adr=0x102, size=2, decpnt=0,
               mode=r.dataMode.numFloat, unit=ru.registerUnits.kWh,
               fixer=rf.readingFixer.round2, enable=True),
   r.register(name=rn.regsNames.L2_TotalActiveEnergy, adr=0x104, size=2, decpnt=0,
               mode=r.dataMode.numFloat, unit=ru.registerUnits.kWh,
               fixer=rf.readingFixer.round2, enable=True),
   r.register(name=rn.regsNames.L3_TotalActiveEnergy, adr=0x106, size=2, decpnt=0,
               mode=r.dataMode.numFloat, unit=ru.registerUnits.kWh,
               fixer=rf.readingFixer.round2, enable=True),
   # - - - read amps ~ current - - -
   r.register(name=rn.regsNames.L1_Current, adr=0x0016, size=2, decpnt=0,
               mode=r.dataMode.numFloat, unit=ru.registerUnits.Amps,
               fixer=rf.readingFixer.round2, enable=True),
   r.register(name=rn.regsNames.L2_Current, adr=0x0018, size=2, decpnt=0,
               mode=r.dataMode.numFloat, unit=ru.registerUnits.Amps,
               fixer=rf.readingFixer.round2, enable=True),
   r.register(name=rn.regsNames.L3_Current, adr=0x001A, size=2, decpnt=0,
               mode=r.dataMode.numFloat, unit=ru.registerUnits.Amps,
               fixer=rf.readingFixer.round2, enable=True)
   )
