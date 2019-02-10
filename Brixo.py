import BGWrapper
from UUID import *

# This module is designed to be used like a singleton class
# It wraps the functions of bglib in an easier to use way

class BrixoStatus:
    def __init__(self, bytevalue):
        self.bytevalue = bytevalue

    def getStandby(self):
        return (self.bytevalue & 0x01 != 0)

    def getCW(self):
        return (self.bytevalue & 0x02 != 0)

    def getCCW(self):
        return (self.bytevalue & 0x04 != 0)

    def getOC(self):
        return (self.bytevalue & 0x08 != 0)

    def getWarning(self):
        return (self.bytevalue & 0x10 != 0)

    def getOverload(self):
        return (self.bytevalue & 0x20 != 0)

    def getUSB(self):
        return (self.bytevalue & 0x40 != 0)

    def getStreaming(self):
        return (self.bytevalue & 0x80 != 0)

class BrixoDevice:
    def __init__(self, ble_dev):
        self.ble_dev = ble_dev
        ble_dev.connect()
        ble_dev.discover()
        ble_dev.enableNotifyForUUID(UUID(0x2B10))
        status = self.getStatus()
        if status.getCW():
            self.channel = 1
        elif status.getCCW():
            self.channel = 2
        elif status.getStandby():
            self.channel = 0
        self.power = 100

    def disconnect(self):
        self.ble_dev.disconnect()

    def setDirection(self, channel, BEEP=1):
        writedata = bytearray('\x61\x70\x70')
        writedata.append('\x63' if BEEP == 1 else '\xE3')
        self.channel = channel
        writedata.append(self.channel)
        writedata.append(self.power)
        writedata += '\r\n'
        self.ble_dev.writecommand(UUID(0x2B11), writedata)

    def standby(self, BEEP=1):
        writedata = bytearray('\x61\x70\x70')
        writedata.append('\x63' if BEEP == 1 else '\xE3')
        writedata += '\x00\x00\r\n'
        self.ble_dev.writecommand(UUID(0x2B11), writedata)

    def setPower(self, pwmratio, BEEP=0):
        writedata = bytearray('\x61\x70\x70')
        writedata.append('\x63' if BEEP == 1 else '\xE3')
        writedata.append(self.channel)
        self.power = pwmratio
        if pwmratio < 0:
            self.power = 0
        if pwmratio > 100:
            self.power = 100
        writedata.append(self.power)
        writedata += '\r\n'
        self.ble_dev.writecommand(UUID(0x2B11), writedata)

    def shutdownBattery(self, BEEP=1):
        writedata = bytearray('\x61\x70\x70')
        writedata.append('\x6F' if BEEP == 1 else '\xEF')
        writedata += '\x66\x66\r\n'
        self.ble_dev.writecommand(UUID(0x2B11), writedata)

    def setTimer(self, cutouttime, BEEP=1):
        writedata = bytearray('\x61\x70\x70')
        writedata.append('\x78' if BEEP == 1 else '\xF8')
        writedata.append(cutouttime / 256)
        writedata.append(cutouttime % 256)
        writedata += '\r\n'
        self.ble_dev.writecommand(UUID(0x2B11), writedata)

    def getStatus(self):
        readdata = self.ble_dev.readNotifyValue(UUID(0x2B10))
        return BrixoStatus(readdata[1])

    def getOutputCurrent(self):
        readdata = self.ble_dev.readNotifyValue(UUID(0x2B10))
        return int(readdata[6]) * 256 + int(readdata[7])

    def getOutputVoltage(self):
        readdata = self.ble_dev.readNotifyValue(UUID(0x2B10))
        return int(readdata[8]) * 256 + int(readdata[9])

    def getTimeLeft(self):
        readdata = self.ble_dev.readNotifyValue(UUID(0x2B10))
        return int(readdata[12]) * 256 + int(readdata[13])

class Brixo:
    def __init__(self, port):
        self.dev_list = {}
        BGWrapper.initialize(port)

    def scan(self, timeout):
        self.dev_list = BGWrapper.scan(timeout)
        return self.dev_list

    def connect(self, mac):
        ble_dev = None
        for b in self.dev_list:
            if b.mac_address() == mac:
                ble_dev = b
                break
        if ble_dev is None:
            return None
        brixo_dev = BrixoDevice(ble_dev)
        return brixo_dev