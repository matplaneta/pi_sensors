#!/usr/bin/python

import re
import os
import subprocess

def readDriverOutput():
	path = os.path.dirname(os.path.realpath(__file__))
	output = subprocess.check_output([path +  "/Adafruit_DHT", "2302", "17"]);
	return output

def readHumidity():

	attemptsCount = 8

	while attemptsCount > 0:
		output = readDriverOutput()
		matches = re.search("Hum =\s+([0-9.]+)", output)
		if (not matches):
			attemptsCount -= 1
			continue

		humidity = float(matches.group(1))
		break

	if attemptsCount == 0:
		raise Exception('sensor unavailable')

	return humidity

def readTemperature():

	attemptsCount = 8

	while attemptsCount > 0:
		output = readDriverOutput()
		matches = re.search("Temp =\s+([0-9.]+)", output)
		if (not matches):
			attemptsCount -= 1
			continue

		t = float(matches.group(1))
		break

	if attemptsCount == 0:
		raise Exception('sensor unavailable')

	return t
