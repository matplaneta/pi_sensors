#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import pytz
import getopt
import db
import os
from datetime import datetime, timedelta
from config import Config

CFG = None

def createGnuplotScript(dateFrom, dateTo, sensor_ids, output):

	dateFromSql = date2Sql(dateFrom)
	dateToSql = date2Sql(dateTo)

	for sid in sensor_ids:
		id = int(sid)
		s = CFG.sensors[id-1]
		min, max = db.getSensorMinMax(id, dateFrom, dateTo)	
		now = db.getSensorLast(id)
#		s['title'] = r'%s\nteraz: %.1f °C\nmax: %.1f °C\nmin: %.1f °C' % (s.label, now, max, min)
		if s.type == 'T':
			unit = '°C'
		else:
			unit = '%'
		s['title'] = r'{1}\nteraz: {2} {0}\nmax: {3} {0}\nmin: {4} {0}'.format(unit, s.label, now, max, min)

	sun = getSunTimes(dateFrom, dateTo + timedelta(days=2))

	weekDays = getWeekDaysTimes(dateFrom, dateTo)

	print 'set terminal png size 1000,500 enhanced font ",11"'
	print 'set output "www/%s"' % output

	print 'set key outside below left horizontal height 5'
	print 'set title "%s"' % (dateTo.strftime("%Y-%m-%d %H:%M"))
	print 'set bmargin 6'

	print 'set datafile separator "|"'
	print 'set style data lines'
	print 'set grid'
	print 'set tic scale 0'
	print 'set locale "pl_PL.UTF-8"'

#	print 'set ylabel "temperatura [°C]" tc rgb "#888888"'
	print 'set y2tics'

	print 'set xdata time'
	print 'set timefmt x "%Y-%m-%d %H:%M"'
	print 'set format x "%H"'

	print 'set x2data time'
	print 'set timefmt x2 "%Y-%m-%d %H:%M"'
	print r'set format x2 "%A\n%d-%m"'
	print 'set x2tics (%s) center offset 0,-1' % weekDays

	print 'set xzeroaxis lt -1 linecolor rgb "blue"'

	i = 1
	while i < len(sun)-1:
		print r'set object rect from %s, graph 0 to %s, graph 1 behind fc rgb "#dddddd" fillstyle solid 0.5 noborder' % (sun[i], sun[i+1])
		i += 2

	sys.stdout.write('plot ')	
	for id in sensor_ids:
		s = CFG.sensors[int(id)-1]
		sys.stdout.write(r'"< sqlite3 sensors.db \"SELECT * FROM sensor%d WHERE date >= %s\"" using 1:2 title "%s" lw 2' % (s.id, dateFromSql, s['title']))
		if id != sensor_ids[-1]: sys.stdout.write(',')
	print ''


def date2Sql(date):
	return date.strftime("'%Y-%m-%d %H:%M'")


def getSunTimes(dateFrom, dateTo):
	import sunrisesunset as ss
    
	sun = []
	d = dateFrom
	delta = timedelta(days=1)
	while d <= dateTo:
		rs = ss.SunriseSunset(d, CFG.latitude, CFG.longitude, 'official')
		riseTime, setTime = rs.getSunRiseSet()
		sun.append(date2Sql(riseTime))
		sun.append(date2Sql(setTime))
		d += delta

	return sun

def getWeekDaysTimes(dateFrom, dateTo):

	p = ''
	if dateFrom.hour >= 12 and dateFrom.hour < 22:
		d = dateFrom.replace(minute=0) + timedelta(hours=2)
		p += date2Sql(d)

	d = dateFrom.replace(hour=12,minute=0)
	delta = timedelta(days=1)
	while d <= dateTo:
		if p != '':
			p += ','
		p += date2Sql(d)
		d += delta

	if dateTo.hour <= 12 and dateTo.hour > 7:
		p += ',' + date2Sql(dateTo.replace(hour=7,minute=0))

	return p


def main(argv):

	HOME = os.path.dirname(os.path.realpath(__file__))
	f = file(HOME+'/sensors.cfg')
	global CFG
	CFG = Config(f)

	tz = pytz.timezone(CFG.timezone)
	dateFrom = datetime.now(tz) - timedelta(days=1)
	dateTo = datetime.now(tz)

	try:
		opts, args = getopt.getopt(argv, "", ["last_days=", "sensor_ids=", "output="])
	except getopt.GetoptError:
		sys.exit(2)

	for opt, arg in opts:
		if opt == "--last_days":
			dt = int(arg)
			dateFrom = datetime.now(tz) - timedelta(days=dt)
		elif opt == "--sensor_ids":
			sensor_ids = arg.split(',')
		elif opt == "--output":
			output = arg

	createGnuplotScript(dateFrom, dateTo, sensor_ids, output)


if __name__ == "__main__":
   main(sys.argv[1:])

