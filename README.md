# BrixoRPi
Connect to Brixo using a computer and the Module Bluetooth, Silicon Labs bled112-v1
Based on the standard free Brixo API formerly available at http://brixotoys.com/pythonapi/ 

The following libraries included here are always needed
UUID.py
bglib.py
BGWrapper.py	

There are two example programs for windows PC and Raspberry Pi , both in python2
Example_PC.py
Example_rpI.py

The modification needed to run the original windows code in linux and RPi is trivial, simply change the use of COM4 by the appropiate /dev/
Here we implement the modification, tested in a RPi3 with Raspbian Stretch using Python 2.7
