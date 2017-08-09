#!/usr/bin/python
import sys 
import os
import json

# Read json config file
def readFile(path):
	with open(path) as file:  
		data = json.load(file)
		return data

# Parse data in config file returning required values
def parseFile(path):
	data = readFile(path)
	id = data["id"]
	serial_port = data['serial_port']
	timeout = data['timeout']
	baud_rate = data['baud_rate']
	return [id, serial_port, baud_rate, timeout]

# Initial configure call to start configuration
def configure():
	path = os.path.dirname(os.path.realpath(__file__)) + "/data.json"
	data = parseFile(path)
	return data

