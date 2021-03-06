import argparse
import os.path
import os
import tempfile
import shutil
import atexit
from datetime import datetime
from time import sleep
import itertools, sys
import time
import threading
from sys import stdin
import glob
from xlsx import printTid
import win32print

class readable_dir(argparse.Action):
    def __call__(self,parser, namespace, values, option_string=None):
        prospective_dir=values
        if not os.path.isdir(prospective_dir):
            raise argparse.ArgumentTypeError("readable_dir:{0} is not a valid path".format(prospective_dir))
        if os.access(prospective_dir, os.R_OK):
            setattr(namespace,self.dest,prospective_dir)
        else:
            raise argparse.ArgumentTypeError("readable_dir:{0} is not a readable dir".format(prospective_dir))


def makeDirectory():
	# print ('make dir')
	# output for today directory
	target_dir =directory + "\\" + "{:%Y-%m-%d}".format(datetime.now())
	if not os.path.exists(target_dir):
		os.makedirs(target_dir)
	success_dir = target_dir +"\\success"
	error_dir = target_dir +"\\error"
	if not os.path.exists(success_dir):
		os.makedirs(success_dir)
	if not os.path.exists(error_dir):
		os.makedirs(error_dir)
	return (success_dir,error_dir)


def run():
	import urllib3
	http = urllib3.PoolManager()
	print ('Intial HTTP successful')
	while True:
		tids = glob.glob(working_dir + '\\*.*')
		# for f in glob.glob(working_dir + '\\*.pdf'):
		# 	print (f)
		if len(tids)>0:
			target_dir =makeDirectory()
			filename=  tids[0]
			head, tail = os.path.split(tids[0])
			
			print ('Print to %s' % printer)
			# clstid= tid(filename)
			print (master_file)
			x=printTid(filename,master_file,target_dir[0],printer)
			result = x.print()

			target_file=target_dir[0] +'\\' + tail
			print (target_file)
			shutil.move(tids[0],target_file )

			# Start close Ticket
			# 1)Check file d:\ticket\tickget.json
			print ('1)Check d:\Tiket.json file')
			fname_ticket= 'd:\\ticket\\ticket.json'
			if os.path.isfile(fname_ticket) :
				print  ('Found ticket ticket file')
				dict = eval(open(fname_ticket).read())
				if 'barcode' in dict:
					ticket = dict['barcode']
					# 2)Get ticket(barcode) from file.
					print ('Current Ticket is %s' % ticket)
					# 3)Post to URL to close Ticket
					url = 'http://192.168.10.54:8080/e-Ticket/checking/activate.php?status=Y&barcode=' + ticket
					r = http.request('GET', url)
					str_r = r.data.decode("utf-8")
					print ('Returned data is  %s' % str_r)
				os.remove(fname_ticket)
				print ('Remove Ticket file--Success!!!')
			# End close Ticket
			
		else:
			print ('File not found : %s' % datetime.now() )

		sleep(5)	


if __name__ == "__main__":
	# TEmporary Directory
	ldir = tempfile.mkdtemp()
	atexit.register(lambda dir=ldir: shutil.rmtree(ldir))

	parser = argparse.ArgumentParser()

	# parser.add_argument('-m','--master', type=argparse.FileType('r', encoding='UTF-8'),
	# 					help="TID master file",required=True)

	parser.add_argument('-p','--printer', default='',
						help="Print to printer")

	parser.add_argument('-i', '--input_directory', action=readable_dir, default=ldir)
	parser.add_argument('-b', '--base_directory', action=readable_dir,default='')


	parser.add_argument("-v", "--verbose", action="store_true",
	                    help="increase output verbosity")
	args = parser.parse_args()
	
	# fSrcExist=args.master

	# print ('Real path file %s' % os.path.dirname(os.path.abspath(__file__)))

	printer=args.printer
	if printer =='':
		printer = win32print.GetDefaultPrinter()

	import json
	based_dir = args.base_directory 
	if based_dir =='' :
		fname = os.path.dirname(os.path.abspath(__file__))  + "\configure.json"
	else :
		fname = based_dir + "\configure.json"

	# print ("Configuration file on : %s" % fname)

	if os.path.isfile(fname) :
		x = open(fname).read()
		j = json.loads(x)
		tid_file_name = j['tid_file']

	# print ('********************************************************************')
	print ('*******************Auto TID Start***********************************')
	print ('Configuration path: %s' % fname)
	print ('Master TID file : %s' % tid_file_name)
	print ('Working Directory : %s' % args.input_directory)
	print ('Printer : %s' % printer)
	print ('********************************************************************')

	# make output in working directory
	success_dir=""
	error_dir = ""
	working_dir = args.input_directory
	master_file = tid_file_name # args.master.name
	# print (printer)
	directory= working_dir +"\output"
	if not os.path.exists(directory):
		os.makedirs(directory)
	
	# --------------------------------

	spinner = itertools.cycle(['-', '/', '|', '\\'])

	run()
