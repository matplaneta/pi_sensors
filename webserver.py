#!/bin/python

import BaseHTTPServer
import os
from urlparse import urlparse, parse_qs
from os import curdir
from config import Config

class WebRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

	def do_GET(self):

		self.send_response(200)

		if self.path.endswith('.png') or self.path.endswith('.ico'):
			self.serveResource('image/png')

		if self.path.endswith('.css'):
			self.serveResource('text/css')

		else:
			self.do_chart()


	def do_chart(self):
		last_days = 1
		try:
			qs = parse_qs(urlparse(self.path).query)
			last_days = qs['last_days'][0]
		except:
			pass

		os.chdir('..')
		os.system('python chart.py --last_days=%s --sensor_ids=1,4 --output=t_outside.png | gnuplot' % last_days)
		os.system('python chart.py --last_days=%s --sensor_ids=2,5 --output=t_inside.png | gnuplot' % last_days)
		os.system('python chart.py --last_days=%s --sensor_ids=6 --output=h_outside.png | gnuplot' % last_days)
		os.chdir('www')
		self.send_header('Content-type',	'text/html')
		self.end_headers()
		f = open('index.html')
		self.wfile.write(f.read())
		f.close()

	def serveResource(self, contentType):
			self.send_header('Content-type', contentType)
			self.end_headers()
			f = open(curdir + self.path)
			self.wfile.write(f.read())
			f.close()


def main():

	HOME = os.path.dirname(os.path.realpath(__file__))
	f = file(HOME+'/sensors.cfg')
	CFG = Config(f)

	try:
		os.chdir(HOME+'/www')
		server = BaseHTTPServer.HTTPServer((CFG.server_address, CFG.server_port), WebRequestHandler)    
		print '%s:%d -> %s\nStarted HTTP server...' % (CFG.server_address, CFG.server_port, HOME)
		server.serve_forever()
	except KeyboardInterrupt:
		print '\nshutting down server'
		server.socket.close()

if __name__ == '__main__':
	main()
