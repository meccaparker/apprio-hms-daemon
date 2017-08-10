#!/usr/bin/env/python

import sys
import os
import datetime
import time
import json
from config import config_daemon as config
import serial_handler
import pi_daemon
import subprocess

# Main function responsible for gathering info and updating database

class Daemon():
	startTime = 0
	endTime = 0
	ID = 0
	serial_port = ""
	baud_rate = 0
	timeout =0

	def initializePortVars(self):
		ID, serial_port, baud_rate, timeout = config.configure()
		self.ID = ID
		self.serial_port = serial_port
		self.baud_rate = baud_rate
		self.timeout = timeout

	def runUpdate(self):
		print("#############################################")
		self.startTime = time.time()
		self.initializePortVars()
		print(datetime.datetime.now())
		print("ID: %d, SERIAL_PORT: %s, BAUDRATE: %d, TIMEOUT: %0.2f" % (self.ID, self.serial_port, self.baud_rate, self.timeout))
		print("Database update for Hub with ID %d initiated." % self.ID)
		self.getHubData(self.ID, self.serial_port, self.baud_rate, self.timeout)

	# Open serial port and query information
	def getHubData(self, ID, serial_port, baud_rate, timeout):
		print("Attempting to retrieve Hub and Pi data...")
		try: 
			def retrieveHubData():
				power, source = "", ""
				temp1 = serial_handler.initiateSerialConn(serial_port, baud_rate, timeout, "power?")
				temp2 = serial_handler.initiateSerialConn(serial_port, baud_rate, timeout, "source?")
				if temp1 == "error" or temp2 == "error":
					raise ValueError
				if temp1 == "timeout" or temp2 == "timeout":
					raise ValueError
				# Parse response
				for c in temp1:
					if c.isdigit():
						power += c
				for c in temp2:
					if c.isdigit():
						source += c
				return power, source
			def retrievePiData():
				piData = pi_daemon.getSystemInfo()
				return piData
			power, source = retrieveHubData()	
			piData = json.loads(retrievePiData())
			system = piData["system"]
			release = piData["release"]
			version = piData["version"]
			machine = piData["machine"]
			processor = piData["processor"]
			hostname = piData["hostname"]
			temperature = piData["temperature"]
			ip_address = piData["ip_address"]
			print("Successfully retrieved Hub and Pi data:")
			print("power = " + str(power))
			print("source = " + str(source))
			print("temperature = " + temperature)
			self.updateDatabase(ID, power, source, temperature)

		except ValueError:
			print("Something went wrong with the serial port. Unable to retrieve Hub data.")
			print("Check unsuccessful.")
			self.endTime = time.time()
			totalTime = self.endTime - self.startTime
			print("[completed in %.1fs]" % totalTime)
			print("#############################################")

	# Open serial port and execute specified command
	def setHubSetting(self, serial_port, baud_rate, timeout, cmd):
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
	def updateDatabase(self, ID, power, source, temperature):
		try: 
			subprocess.call(["node", "db_check", str(ID), str(power), str(source), temperature])
			print("Check successful.")
			self.endTime = time.time()
			totalTime = self.endTime - self.startTime
			print("[completed in %.1fs]" % totalTime)
			print("#############################################")
		except:
			print("Something went wrong with the database. Check unsuccessful.")
			self.endTime = time.time()
			totalTime = self.endTime - self.startTime
			print("[completed in %.1fs]" % totalTime)
			print("#############################################")

if __name__ == "__main__":
	try:
		cmd = sys.argv[1]
		ID, serial_port, baud_rate, timeout = config.configure()
		daemon = Daemon()
		output = daemon.setHubSetting(serial_port, baud_rate, timeout, cmd)
		print(output)
	except:
		daemon = Daemon()
		daemon.runUpdate()

