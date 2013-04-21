#!/usr/bin/python
# -*- coding: utf-8 -*-

import db
import w1
import dht
import logging
import lcd
import RPi.GPIO as GPIO
import pytz
import os
from datetime import datetime
from config import Config


def main():

	HOME = os.path.dirname(os.path.realpath(__file__))
	f = file(HOME+'/sensors.cfg')
	CFG = Config(f)
	logging.basicConfig(filename=HOME+'/sensors.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M')

	tz = pytz.timezone(CFG.timezone)
	date = datetime.now(tz)

	GPIO.setwarnings(False)
	m = date.strftime("%Y-%m-%d\n%H:%M:%S")
	lcd.init()
	lcd.message(m)

	if date.hour >= 0 and date.hour <= 5:
		lcd.backlight(False)
	else:
		lcd.backlight(True)

	d = [] # read sensor data
	for s in CFG.sensors:

		if s.id < 0: continue # skip disabled sensors

		try:
			if s.name == 'DS18B20':
				v = w1.readTemp(s.rom_code)
			elif s.name == 'DHT22' and s.rom_code == 'H':
				v = dht.readHumidity()
			elif s.name == 'DHT22' and s.rom_code == 'T':
				v = dht.readTemperature()
			else:
				raise Exception('unknown sensor name')
				continue
		except Exception as e:
			logging.error("| Can't read sensor %d | %s | %s" % (s.id, s.rom_code, str(e)))
			continue

		try:
			db.updateSensor(s.id, v, date)
			if(s.type == 'H'):
				d.append('%d%%' % v)
			else:
				d.append(v)
#			print "#%d %s, %s: %.1f" % (s.id, s.rom_code, s.label, v)
		except Exception as e:
			logging.error("| Can't update sensor %d | %s | %s" % (s.id, s.rom_code, str(e)))
			continue

	m = buildMessage(d, date)	
	lcd.message(m)


def buildMessage(d, date):
	time = date.strftime("%H:%M")
	m = ''
	i = 0
	while i < len(d) and i <= 5:
		m += str(d[i]) + ' '
		if i == 1:
			m = m.ljust(16-len(time), ' ') + time + '\n'
		i += 1

	return m

if __name__ == "__main__":
	main()
