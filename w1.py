#!/usr/bin/python

import re

def readTemp(romCode):

	pCrc = re.compile('crc=\w+\s(YES|NO)')
	crc = 'NO'
	attemptsCount = 8

	while crc == 'NO' and attemptsCount > 0:
		f = open('/sys/bus/w1/devices/' + romCode + '/w1_slave', 'r')
		lineCrc = f.readline()
		lineTemp = f.readline()
		f.close()
		attemptsCount -= 1
		mCrc = pCrc.search(lineCrc)
		if mCrc:
			crc = mCrc.group(1)

	if attemptsCount == 0:
		raise Exception('bad CRC')

	pTemp = re.compile('.*\st=(\-\d+|\d+)')	
	mTemp = pTemp.search(lineTemp)
	if mTemp:
		t = float(mTemp.group(1)) / 1000
		return round(t,1)

	raise Exception("can't parse: " + lineTemp)
