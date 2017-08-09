#!/usr/bin/env/python

import serial
import time
import sys

class SerialPortHandler:
    serial = None
    portName = ""
    baudrate = 0
    timeout = 0

    def __init__(self, portName, baudrate, timeout):
        try: # Try opening a port
            self.portName = portName
            self.baudrate = baudrate
            self.timeout = timeout
            self.serial = self.openPort()
        except:
            exit()
            return ""

    # Open a serial port
    def openPort(self):
        serialPort = serial.Serial() 
        serialPort.port = self.portName
        serialPort.baudrate= self.baudrate 
        serialPort.timeout = self.timeout # in seconds
        return serialPort

    def sendCommand(self, cmd):
        # Check if a port is open.
        if not self.serial.isOpen(): 
            # If port isn't open for some reason, open it.
            try: 
                self.serial.open()
            # If port can't be opened, open a new one altogether.
            except: 
                self.serial = self.openPort()
        while True:
             # Close the port when exit command received.
            if cmd == "exit":
                self.serial.close()
                return ""
            else:
                try:
                     # Write the command to the serial port.
                    self.serial.write(cmd + "\r")
                    output = self.serial.readlines()
                    self.serial.close()
                    if output == "":
                        return "error"
                    else:
                        return output
                except:
                    return "error"


def initiateSerialConn(port, baudrate, timeout, cmd):
    serialPortHandler = SerialPortHandler(port, baudrate, timeout)
    output = serialPortHandler.sendCommand(cmd)
    if type(output) == str:
        return output
    else:
        return " ".join(output).strip()

if __name__ == "__main__":
    port = "/dev/tty.usbserial"
    baudrate = 115200
    timeout = 0.05
    cmd = "power"
    a = initiateSerialConn(port, baudrate, timeout, cmd)
    print(a)
