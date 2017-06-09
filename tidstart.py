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
# from TIDclass import tid
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

class Spinner:
    busy = False
    delay = 0.1

    @staticmethod
    def spinning_cursor():
        while 1: 
            for cursor in '|/-\\': yield cursor

    def __init__(self, delay=None):
        self.spinner_generator = self.spinning_cursor()
        if delay and float(delay): self.delay = delay

    def spinner_task(self):
        while self.busy:
            sys.stdout.write(next(self.spinner_generator))
            sys.stdout.flush()
            time.sleep(self.delay)
            sys.stdout.write('\b')
            sys.stdout.flush()

    def start(self):
        self.busy = True
        threading.Thread(target=self.spinner_task).start()

    def stop(self):
        self.busy = False
        time.sleep(self.delay)


# while True:
# 	# sys.stdout.write(next(spinner))
# 	# sys.stdout.flush()
# 	# sys.stdout.write('\b')
# 	# sleep(0.2)

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
	while True:
		tids = glob.glob(working_dir + '\\*.pdf')
		# for f in glob.glob(working_dir + '\\*.pdf'):
		# 	print (f)
		if len(tids)>0:
			target_dir =makeDirectory()
			filename=  tids[0]
			head, tail = os.path.split(tids[0])
			
			print ('Print to %s' % printer)
			# clstid= tid(filename)
			# print (clstid.getInfo())
			x=printTid(filename,master_file,target_dir[0],printer)
			x.print()
			
			target_file=target_dir[0] +'\\' + tail
			print (target_file)
			shutil.move(tids[0],target_file )
		else:
			print ('File not found : %s' % datetime.now() )

		sleep(5)	
		# try:
		# 	# Check pdf in working folder
		# 	tids = os.listdir(working_dir) #include 'output'
		# 	if len(tids)>1:
		# 		target_dir =makeDirectory()
		# 		filename= working_dir + '\\' + tids[0]
		# 		clstid= tid(filename)
		# 		print (clstid.getInfo())
				
		# 		target_file=target_dir[0] +'\\' +tids[0]
		# 		print (target_file)
		# 		shutil.move(filename,target_file )
		# 	else:
		# 		print ('File not found : %s' % datetime.now() )

		# 	sleep(5)
		# except Exception:
		# 	# spinner.stop()
		# 	print ('Bye bye')
		# 	return
		#This won't catch KeyboardInterupt
		
		# choice = input()
		# if choice == "a":
		# 	print ("Type A")
		# elif choice == "q":
		# 	print ("Bye Bye")
		# return

if __name__ == "__main__":
	# TEmporary Directory
	ldir = tempfile.mkdtemp()
	atexit.register(lambda dir=ldir: shutil.rmtree(ldir))

	parser = argparse.ArgumentParser()
	parser.add_argument('-m','--master', type=argparse.FileType('r', encoding='UTF-8'),
						help="TID master file",required=True)
	parser.add_argument('-p','--printer', default='',
						help="Print to printer")

	parser.add_argument('-i', '--input_directory', action=readable_dir, default=ldir)

	# parser.add_argument("square", type=int,
	#                     help="display a square of a given number")
	parser.add_argument("-v", "--verbose", action="store_true",
	                    help="increase output verbosity")
	args = parser.parse_args()
	# answer = args.square**2
	fSrcExist=args.master
	printer=args.printer
	if printer =='':
		printer = win32print.GetDefaultPrinter()

	# print ('********************************************************************')
	print ('*******************Auto TID Start***********************************')
	print ('Master TID file : %s' % args.master.name)
	print ('Working Directory : %s' % args.input_directory)
	print ('Printer : %s' % printer)
	print ('********************************************************************')

	# make output in working directory
	success_dir=""
	error_dir = ""
	working_dir = args.input_directory
	master_file = args.master.name
	# print (printer)
	directory= working_dir +"\output"
	if not os.path.exists(directory):
		os.makedirs(directory)
	
	# --------------------------------

	spinner = itertools.cycle(['-', '/', '|', '\\'])

	run()




	# print (datetime.now())
	# sleep(5)
# if args.verbose:
#     print ("the square of {} equals {}".format(args.square, answer))
# else:
#     print (answer)



# import os.path
# from shutil import copyfile
# from datetime import datetime
# from time import sleep

# folder_src="D:\\sample_autofit\\"
# folder_dst="T:\\_C\\ChutchaiS\\LOGS\\"
# # check Target
# while True:
# 	fname="{:%Y-%m-%d}".format(datetime.now())+".txt"
# 	fname_src = folder_src + fname
# 	fname_dst = folder_dst + fname
# 	fSrcExist=os.path.isfile(fname_src)

# 	if fSrcExist:
# 		copyfile(fname_src,fname_dst)
# 		print ("Copy file " + fname + " Successful!!!")
# 	else:
# 		print ("File Not found " + fname_src )

# 	sleep(5)