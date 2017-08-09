#!/usr/bin/env/python

import sys
import os
import datetime
import time
from config import config_daemon as config
import serial_handler

# Main function responsible for gathering info and updating database
def runUpdate():
	startTime = time.time()
	ID, serial_port, baud_rate, timeout = config.configure()
	print("#############################################")
	print(datetime.datetime.now())
	print("ID: %d, SERIAL_PORT: %s, BAUDRATE: %d, TIMEOUT: %0.2f" % (ID, serial_port, baud_rate, timeout))
	print("Database update for Hub with ID %d initiated." % ID)
	getHubData(ID, serial_port, baud_rate, timeout)
	endTime = time.time()
	totalTime = endTime - startTime
	print("[completed in %.1fs]" % totalTime)
	print("#############################################")

# Open serial port and query information
def getHubData(ID, serial_port, baud_rate, timeout):
	print("Attempting to retrieve Hub data...")
	try: 
		def getData():
			power, source = "", ""
			temp1 = serial_handler.initiateSerialConn(serial_port, baud_rate, timeout, "power?")
			temp2 = serial_handler.initiateSerialConn(serial_port, baud_rate, timeout, "source?")
			# Parse response
			for c in temp1:
				if c.isdigit():
					power += c
			for c in temp2:
				if c.isdigit():
					source += c
			return power, source
		power, source = getData()
		# power, source = 100,100
		if power == "timeout" or source == "timeout":
			raise ValueError()
		else:
			print("Successfully retrieved Hub data:")
			print("power = " + str(power))
			print("source = " + str(source))
			updateDatabase(ID, power, source)
	except ValueError:
		print("Something went wrong with the serial port. Unable to retrieve Hub data.")
		print("Check unsuccessful.")

# Open serial port and execute specified command
def setHubSetting(serial_port, baud_rate, timeout, cmd):
	try:
		def putData():
			output = ""
			temp = serial_handler.initiateSerialConn(serial_port, baud_rate, timeout, cmd)
			# Parse response
			if temp == 'error':
				return temp
			for c in temp:
				if c.isdigit():
					output += c
			return output
		output = putData()
		if output == "timeout":
			raise ValueError
		else:
			return output
	except:
		print("error")
		return "error"

# Update database with new info
def updateDatabase(ID, power, source):
	try: 
		os.system("node db_check %d %s %s" % (ID, power, source))
		print("Check successful.")
	except:
		print("Something went wrong with the database. Check unsuccessful.")

if __name__ == "__main__":
	try:
		cmd = sys.argv[1]
		ID, serial_port, baud_rate, timeout = config.configure()
		output = setHubSetting(serial_port, baud_rate, timeout, cmd)
		print(output)
	except:
		runUpdate()

