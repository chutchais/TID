import sys,getopt
import xlsxwriter
from openpyxl import load_workbook
from TIDclass import tid

import tempfile
import win32api
import win32print
import os


class printTid:
	def __init__(self, filename,masterfile,targetDir,printer=''):
		self.filename = filename
		self.master_file = masterfile
		self.targetDir = targetDir
		self.printer = printer


	def print(self):
		# print ('Hello %s' % argv[0] )
		tid_data= tid(self.filename)
		data = tid_data.getInfo()

		print(data)

		xfile = load_workbook(self.master_file)
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
					sheet['C3'] = item_ins[item]['location']
					sheet['I3'] = item_ins[item]['container_no']
					sheet['I4'] = item_ins[item]['seal']
					vFirst=False
				else:
					sheet['C8'] = item_ins[item]['location']
					sheet['I8'] = item_ins[item]['container_no']
					sheet['I9'] = item_ins[item]['seal']

		if 'out' in data:
			item_ins =data['out']
			vFirst=True
			for item in item_ins:
				if vFirst:
					sheet['C14'] = item_ins[item]['location']
					sheet['I14'] = item_ins[item]['container_no']
					sheet['I15'] = item_ins[item]['seal']
					sheet['I16'] = item_ins[item]['line3']
					vFirst=False
				else:
					sheet['C19'] = item_ins[item]['location']
					sheet['I19'] = item_ins[item]['container_no']
					sheet['I20'] = item_ins[item]['seal']
					sheet['I21'] = item_ins[item]['line3']


		targetFile = self.targetDir + '\\' + os.path.split(self.filename)[1].replace('.pdf','.xlsx')
		xfile.save(targetFile)
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

