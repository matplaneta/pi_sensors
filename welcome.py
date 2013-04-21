#!/usr/bin/python

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

	tz = pytz.timezone(CFG.timezone)
	date = datetime.now(tz)

	GPIO.setwarnings(False)
	lcd.init()
	lcd.message('Raspberry Pi\n%s' % date.strftime("%Y-%m-%d %H:%M"))
	lcd.backlight(True)

if __name__ == "__main__":
	main()
