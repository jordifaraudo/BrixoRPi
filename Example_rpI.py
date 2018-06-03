import BGWrapper
from UUID import *
from Brixo import *

def printMenu():
    print "0: setDirection"
    print "1: standby"
    print "2: setPower"
    print "3: shutdownBattery"
    print "4: setTimer"
    print "5: get data functions"
    print "q: Quit"

if __name__=="__main__":
    # Set up the lower level to talk to a BLED112 in port COM4
    # REPLACE THIS WITH THE BLED112 PORT ON YOUR SYSTEM
    brixo = Brixo("/dev/ttyACM0")

    print("Scanning...")
    # Scan for 3 seconds
    scan_results = brixo.scan(3)
    if len(scan_results) == 0:
        print("Device not found")
        exit(0)

    print("Found %d Device(s)" % len(scan_results))

    # Print found devices
    for i in range(len(scan_results)):
        print "[%d] %s" % (i, scan_results[i].mac_address())

    # Select a device
    dev_id = ''
    while True:
        dev_id = raw_input("Select device:")
        if dev_id == 'Q' or dev_id == 'q':
            exit(0)

        if int(dev_id) >= len(scan_results):
            print ("Range error, input again.")
            continue
        break

    dev_id = int(dev_id)

    # Connect the device using MAC address
    # I think I can use this to connect several devices
    brixo_dev = brixo.connect(scan_results[dev_id].mac_address())

    beep = 1
    # Write command to the device
    while True:
        printMenu()
        selection = raw_input("Input Command: ")
        if selection == 'q' or selection == 'Q':
            brixo_dev.disconnect()
            break
        selectid = int(selection)
        if selectid == 0:
            channel = raw_input("Input Channel (1:CW, 2:CCW): ")
            brixo_dev.setDirection(int(channel), beep)
        elif selectid == 1:
            brixo_dev.standby(beep)
        elif selectid == 2:
            power = raw_input("Input Power (0-100): ")
            brixo_dev.setPower(int(power), beep)
        elif selectid == 3:
            brixo_dev.shutdownBattery(beep)
        elif selectid == 4:
            timervalue = raw_input("Input Cutout Time (0-65535): ")
            brixo_dev.setTimer(int(timervalue))
        elif selectid == 5:
            print "getStatus() Result: "
            status = brixo_dev.getStatus()
            print "Standby  : " + str(status.getStandby())
            print "CW       : " + str(status.getCW())
            print "CCW      : " + str(status.getCCW())
            print "OC       : " + str(status.getOC())
            print "Warning  : " + str(status.getWarning())
            print "Overload : " + str(status.getOverload())
            print "USBSource: " + str(status.getUSB())
            print "Streaming: " + str(status.getStreaming())

            print ""
            print "Output Current: " + str(brixo_dev.getOutputCurrent()) + " mA"
            print "Output Voltage: " + str(brixo_dev.getOutputVoltage() * 10) + " mV"
            print "Time Left     : " + str(brixo_dev.getTimeLeft()) + " s"
