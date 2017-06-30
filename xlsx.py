import sys,getopt
import xlsxwriter
from openpyxl import load_workbook
from TIDclass3 import tid

import tempfile
import win32api
import win32print
import os
import re

class printTid:
	def __init__(self, filename,masterfile,targetDir,printer=''):
		self.filename = filename
		self.master_file = masterfile
		self.targetDir = targetDir
		self.printer = printer

	def convert_location(self,location):
		rex1 = re.compile("^[0-9]{2}[A-Z][0-9]{2}[A-Z][0-9]$")
		rex2 = re.compile("^[0-9]{2}[A-Z][0-9]{4}[A-Z][0-9]$")
		if rex1.match(location) :
			print ('Match Location')
			return  location[:3] + '-' + location[3:5]

		if rex2.match(location) :
			print ('Match Location')
			return  location[:3] + '-' + location[3:5] + '-' + location[5:7]

		return location



	def print(self):
		# print ('Hello %s' % argv[0] )
		# Get TID XLS file from tid.json file
		import json
		fname ='tid.json'
		if os.path.isfile(fname) :
			x = open(fname).read()
			j = json.loads(x)
			tid_file_name = j['tid_file']
			print ('TID file name from tid.json : %s' % tid_file_name)
		#=========================================
		only_filename = os.path.split(self.filename)[1]
		head,tail = os.path.splitext(self.filename)
		tid_data= tid(self.filename)
		data = tid_data.getInfo()

		print(data)

		xfile = load_workbook(tid_file_name)
		sheet = xfile.get_sheet_by_name('master')

		# Fill Master data
		sheet['A1'] = data['time_stamp']
		sheet['D1'] = data['company']
		sheet['J1'] = data['license_no']
		sheet['C24'] = data['call_card']

		if 'in' in data:
			item_ins =data['in']
			vFirst=True
			for item in item_ins:
				if vFirst:
					sheet['C3'] = self.convert_location(item_ins[item]['location'])
					sheet['C6'] = item_ins[item]['location']
					sheet['I3'] = item_ins[item]['container_no']
					sheet['I4'] = item_ins[item]['seal']
					sheet['L4'] = item_ins[item]['seal2']
					vFirst=False
				else:
					sheet['C8'] = self.convert_location(item_ins[item]['location'])
					sheet['C11'] = item_ins[item]['location']
					sheet['I8'] = item_ins[item]['container_no']
					sheet['I9'] = item_ins[item]['seal']
					sheet['L9'] = item_ins[item]['seal2']

		if 'out' in data:
			item_ins =data['out']
			vFirst=True
			for item in item_ins:
				if vFirst:
					sheet['C14'] = self.convert_location(item_ins[item]['location'])
					sheet['C17'] = item_ins[item]['location']
					sheet['I14'] = item_ins[item]['container_no']
					sheet['I15'] = item_ins[item]['seal']
					sheet['I16'] = item_ins[item]['line3']
					vFirst=False
				else:
					sheet['C19'] = self.convert_location(item_ins[item]['location'])
					sheet['C22'] = item_ins[item]['location']
					sheet['I19'] = item_ins[item]['container_no']
					sheet['I20'] = item_ins[item]['seal']
					sheet['I21'] = item_ins[item]['line3']


		targetFile = self.targetDir + '\\' + os.path.split(self.filename)[1].replace('.','') +'.xlsx'
		print ('Target file %s' % targetFile)
		xfile.save(targetFile)
		xfile.close()
		# xfile = None
		# sheet.Close()
		# xfile.Close()
		default_printer =  win32print.GetDefaultPrinter()
		if self.printer == '' :
			curr_printer = default_printer
		else:
			curr_printer=self.printer
			win32print.SetDefaultPrinter(curr_printer)
		

		win32api.ShellExecute (
					  0,
					  "print",
					  targetFile,
					  #
					  # If this is None, the default printer will
					  # be used anyway.
					  #
					  '/d:"%s"' % curr_printer,
					  ".",
					  0
					)

		win32print.SetDefaultPrinter(default_printer) #set default back to original

		print ('Print successful!!')

# if __name__ == "__main__":
#     sys.exit(main(sys.argv[1:]))

