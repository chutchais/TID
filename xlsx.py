import sys,getopt
# import xlsxwriter
# from openpyxl import load_workbook
from TIDclass3 import tid

import tempfile
# import win32api
# import win32print
import os
import re

import redis
import json

class printTid:
	def __init__(self, filename,masterfile,targetDir,printer='',computer=''):
		self.filename = filename
		self.master_file = masterfile
		self.targetDir = targetDir
		self.printer = printer
		self.computer = computer

	def print(self):
		try:
			db = redis.StrictRedis('192.168.10.102', 6379, charset="utf-8", decode_responses=True)
			#=========================================
			only_filename = os.path.split(self.filename)[1]
			head,tail = os.path.splitext(self.filename)
			tid_data= tid(self.filename)
			data = tid_data.getInfo()
			# print(data)
			import json
			lpn = data['license']
			ttl =3600
			db.set(lpn,json.dumps(data) ) #store dict in a hashjson.dumps(json_data)
			db.expire(lpn, ttl) #expire in hour
			db.publish(self.computer.lower(),lpn)

			print('Sent completed. and publish to %s' % self.computer.lower())
			print ('Print successful!!')
		except :
			print ('Error on Print function')


