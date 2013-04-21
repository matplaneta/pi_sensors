#!/usr/bin/python

import sqlite3
import os

DB = os.path.dirname(os.path.realpath(__file__)) + '/sensors.db'

def updateSensor(sensorId, t, date):

	dateStr = date.strftime("%Y-%m-%d %H:%M")

	conn = sqlite3.connect(DB)
	c = conn.cursor()
	tableName = "sensor" + str(sensorId)
	c.execute("INSERT INTO " + tableName + " VALUES(?, ?)",[dateStr, t])
	conn.commit()
	c.close()


def getSensorMinMax(sensorId, dateFrom, dateTo):

	conn = sqlite3.connect(DB)
	c = conn.cursor()
	sql = "SELECT MIN(value), MAX(value) FROM sensor%d WHERE date >= '%s'" % (sensorId, dateFrom.strftime("%Y-%m-%d %H:%M"))
	c.execute(sql)
	min, max = c.fetchone()
	c.close()
	return min, max


def getSensorLast(sensorId):

	conn = sqlite3.connect(DB)
	c = conn.cursor()
	sql = "SELECT value FROM sensor%d ORDER BY date DESC LIMIT 1" % sensorId
	c.execute(sql)
	v = c.fetchone()[0]
	c.close()
	return v

