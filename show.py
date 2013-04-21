#!/usr/bin/python

import db
import w1
import dht
import logging
import lcd
import RPi.GPIO as GPIO
import pytz
import os
import scan
from datetime import datetime
from config import Config
from time import sleep

def main():

	HOME = os.path.dirname(os.path.realpath(__file__))
	f = file(HOME+'/sensors.cfg')
	CFG = Config(f)
	logging.basicConfig(filename=HOME+'/sensors.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M')

	tz = pytz.timezone(CFG.timezone)
	date = datetime.now(tz)

	m = date.strftime("%Y-%m-%d\n%H:%M:%S")
	GPIO.setwarnings(False)
	lcd.init()
	lcd.backlight(True)
	lcd.message(m)

	d = [] # read sensor data
	for s in CFG.sensors:

		if s.id < 0: continue # skip disabled sensors

		try:
			if s.name == 'DS18B20':
				v = w1.readTemp(s.rom_code)
			elif s.name == 'DHT22' and s.type == 'H':
				v = dht.readHumidity()
			elif s.name == 'DHT22' and s.type == 'T':
				v = dht.readTemperature()
			else:
				raise Exception('unknown sensor name')
				continue
		except Exception as e:
			logging.error("| Can't read sensor %d | %s | %s" % (s.id, s.rom_code, str(e)))
			continue

		try:
			print "%s, %s: %.1f" % (s.rom_code, s.label, v)
			if(s.type == 'H'):
				d.append('%d%%' % v)
			else:
				d.append(v)			
		except Exception as e:
			print "Can't print sensor %d" % s.id

	m = scan.buildMessage(d, date)
	lcd.message(m)

if __name__ == "__main__":
	main()
