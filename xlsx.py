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

	# def convert_location(self,location):
	# 	rex1 = re.compile("^[0-9]{2}[A-Z][0-9]{2}[A-Z][0-9]$")
	# 	rex2 = re.compile("^[0-9]{2}[A-Z][0-9]{4}[A-Z][0-9]$")
	# 	if rex1.match(location) :
	# 		print ('Match Location')
	# 		return  location[:3] + '-' + location[3:5]

	# 	if rex2.match(location) :
	# 		print ('Match Location')
	# 		return  location[:3] + '-' + location[3:5] + '-' + location[5:7]

	# 	return location

	# def download_QRcode_img(self,data,server='http://192.168.10.20:8010/',img_size=200):
	# 	# start = time.time()
	# 	if data != '':
	# 		from io import BytesIO
	# 		# from StringIO import StringIO
	# 		import urllib3
	# 		import cv2
	# 		from PIL import Image
	# 		# from urllib3 import urlretrieve
	# 		http = urllib3.PoolManager()
	# 		headers = urllib3.util.make_headers(basic_auth='gate:lcb12017')
	# 		r = http.request('GET', 
	# 				server + data,
	# 				preload_content=False,
	# 				headers=headers)
	# 		# r = http.request('GET', 'http://127.0.0.1:8000/media/images/LCB1/2018/4/20/side0.jpg',preload_content=False)
	# 		img = Image.open(BytesIO(r.data))
	# 		# img.save('driver.png')
	# 		# 400,225
	# 		img_thumbnail = img.resize((img_size,img_size),Image.ANTIALIAS)
	# 		img_thumbnail.save(data + '.png')
	# 		# end = time.time()
	# 		# print('Download time : %s sec(s)' % (end - start))
	# 		return True

	def print(self):
		db = redis.StrictRedis('192.168.10.102', 6379, charset="utf-8", decode_responses=True)
		# print ('Hello %s' % argv[0] )
		# Get TID XLS file from tid.json file
		# import json
		# fname ='configure.json'
		# if os.path.isfile(fname) :
		# 	x = open(fname).read()
		# 	j = json.loads(x)
		# 	tid_file_name = j['tid_file']
		# 	print ('TID file name from tid.json : %s' % tid_file_name)
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
		# sys.exit()

		
		# print ('Master file %s' % self.master_file)

		# import json
		# fname = "configure.json"

		# # default value
		# qr_server='http://192.168.10.20:8010/'
		# qr_size ='200'
		# qr_cell = 'A1'
		# # # Master data
		# # cell_time_stamp		= 'A1'
		# # cell_company 		= 'D1'
		# # cell_license		= 'J1'
		# # cell_call_card		= 'C24'

		# # from configuration
		# if os.path.isfile(fname) :
		# 	x = open(fname).read()
		# 	j = json.loads(x)
		# 	qr_server = j['QR']
		# 	qr_size = j['QR_size']
		# 	qr_cell = j['cell_QR']
		# 	# Master data
		# 	cell_time_stamp		= j['cell_time_stamp']
		# 	cell_company 		= j['cell_company']
		# 	cell_license		= j['cell_license']
		# 	cell_call_card		= j['cell_call_card']
		# 	# IN
		# 	cell_in1_loc		= j['cell_in1_loc']
		# 	cell_in1_loc_short	= j['cell_in1_loc_short']
		# 	cell_in1_container	= j['cell_in1_container']
		# 	cell_in1_seal1		= j['cell_in1_seal1']
		# 	cell_in1_seal2		= j['cell_in1_seal2']
		# 	cell_in1_damage		= j['cell_in1_damage']

		# 	cell_in2_loc		= j['cell_in2_loc']
		# 	cell_in2_loc_short	= j['cell_in2_loc_short']
		# 	cell_in2_container	= j['cell_in2_container']
		# 	cell_in2_seal1		= j['cell_in2_seal1']
		# 	cell_in2_seal2		= j['cell_in2_seal2']
		# 	cell_in2_damage		= j['cell_in2_damage']

		# 	# OUT
		# 	cell_out1_loc		= j['cell_out1_loc']
		# 	cell_out1_loc_short	= j['cell_out1_loc_short']
		# 	cell_out1_container	= j['cell_out1_container']
		# 	cell_out1_seal1		= j['cell_out1_seal1']
		# 	cell_out1_line3		= j['cell_out1_line3']
		# 	cell_out1_damage	= j['cell_out1_damage']

		# 	cell_out2_loc		= j['cell_out2_loc']
		# 	cell_out2_loc_short	= j['cell_out2_loc_short']
		# 	cell_out2_container	= j['cell_out2_container']
		# 	cell_out2_seal1		= j['cell_out2_seal1']
		# 	cell_out2_line3		= j['cell_out2_line3']
		# 	cell_out2_damage	= j['cell_out2_damage']

		

		# # Dowload QR Code
		# qr_image_download = self.download_QRcode_img(data['call_card'],qr_server,qr_size)
		# # sys.exit()
		# # ---------------

		# xfile = load_workbook(self.master_file)
		# sheet = xfile.get_sheet_by_name('master')

		# # Fill Master data
		# sheet[cell_time_stamp] = data['time_stamp']
		# sheet[cell_company] = data['company']
		# sheet[cell_license] = data['license_no']
		# sheet[cell_call_card] = data['call_card']
		# # sheet['A24'] = '*' + data['call_card'] + '*'

		# # Add image to Sheet
		# if qr_image_download :
		# 	import openpyxl
		# 	img = openpyxl.drawing.image.Image(data['call_card'] +'.png')
		# 	sheet.add_image(img, qr_cell)
		# # -----------------


		# if 'in' in data:
		# 	item_ins =data['in']
		# 	vFirst=True
		# 	for item in item_ins:
		# 		if vFirst:
		# 			sheet[cell_in1_loc_short] 	= self.convert_location(item_ins[item]['location'])
		# 			sheet[cell_in1_loc] 		= item_ins[item]['location']
		# 			sheet[cell_in1_container] 	= item_ins[item]['container_no']
		# 			sheet[cell_in1_seal1] 		= item_ins[item]['seal']
		# 			sheet[cell_in1_seal2] 		= item_ins[item]['seal2']
		# 			sheet[cell_in1_damage] 		= item_ins[item]['damage']
		# 			vFirst=False
		# 		else:
		# 			sheet[cell_in2_loc_short] 	= self.convert_location(item_ins[item]['location'])
		# 			sheet[cell_in2_loc] 		= item_ins[item]['location']
		# 			sheet[cell_in2_container] 	= item_ins[item]['container_no']
		# 			sheet[cell_in2_seal1] 		= item_ins[item]['seal']
		# 			sheet[cell_in2_seal2] 		= item_ins[item]['seal2']
		# 			sheet[cell_in2_damage] 		= item_ins[item]['damage']

		# if 'out' in data:
		# 	item_ins =data['out']
		# 	vFirst=True
		# 	for item in item_ins:
		# 		if vFirst:
		# 			sheet[cell_out1_loc_short] 	= self.convert_location(item_ins[item]['location'])
		# 			sheet[cell_out1_loc] 		= item_ins[item]['location']
		# 			sheet[cell_out1_container] 	= item_ins[item]['container_no']
		# 			sheet[cell_out1_seal1] 		= item_ins[item]['seal']
		# 			sheet[cell_out1_line3] 		= item_ins[item]['line3']
		# 			sheet[cell_out1_damage] 	= item_ins[item]['damage']
		# 			vFirst=False
		# 		else:
		# 			sheet[cell_out2_loc_short] 	= self.convert_location(item_ins[item]['location'])
		# 			sheet[cell_out2_loc]		= item_ins[item]['location']
		# 			sheet[cell_out2_container] 	= item_ins[item]['container_no']
		# 			sheet[cell_out2_seal1] 		= item_ins[item]['seal']
		# 			sheet[cell_out2_line3] 		= item_ins[item]['line3']
		# 			sheet[cell_out2_damage] 	= item_ins[item]['damage']


		# targetFile = self.targetDir + '\\' + os.path.split(self.filename)[1].replace('.','') +'.xlsx'
		# print ('Target file %s' % targetFile)
		# xfile.save(targetFile)
		# xfile.close()
		# # xfile = None
		# # sheet.Close()
		# # xfile.Close()
		# default_printer =  win32print.GetDefaultPrinter()
		# if self.printer == '' :
		# 	curr_printer = default_printer
		# else:
		# 	curr_printer=self.printer
		# 	win32print.SetDefaultPrinter(curr_printer)
		

		# win32api.ShellExecute (
		# 			  0,
		# 			  "print",
		# 			  targetFile,
		# 			  #
		# 			  # If this is None, the default printer will
		# 			  # be used anyway.
		# 			  #
		# 			  '/d:"%s"' % curr_printer,
		# 			  ".",
		# 			  0
		# 			)

		# win32print.SetDefaultPrinter(default_printer) #set default back to original

		print ('Print successful!!')

# if __name__ == "__main__":
#     sys.exit(main(sys.argv[1:]))

