import sys,getopt
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure, LTImage, LTChar
import json


class tid:
	def __init__(self, filename):
		self.filename = filename

	# @staticmethod	

	def get_layout_count(self,layout):
		return len(layout)


	def get_line_text(self,layout,line_number):
		i=1
		for lt_obj in layout:
			if isinstance(lt_obj, LTTextBox) :
				if i==line_number :
					# print('--in function--%s' % i)
					x=lt_obj.get_text()
					return x.strip()
				i=i+1
		return ''

	def getInfo(self):
		fp = open(self.filename, 'rb')
		parser = PDFParser(fp)
		doc = PDFDocument()
		parser.set_document(doc)
		doc.set_parser(parser)
		doc.initialize('')
		rsrcmgr = PDFResourceManager()
		laparams = LAParams()
		device = PDFPageAggregator(rsrcmgr, laparams=laparams)
		interpreter = PDFPageInterpreter(rsrcmgr, device)
		# Process each page contained in the document.
		images_folder=""
		text_content = []
		# print ("Info")
		import re
		rex = re.compile("^[0-9]{2}[A-Z][0-9]{2}[A-Z][0-9]$")

		for page in doc.get_pages():
			interpreter.process_page(page)
			layout = device.get_result()
			layout_count = self.get_layout_count(layout)
			i=1

			# print ('LayOut Count : %s' % layout_count)
			# if layout_count =9 , means Full1Box (IN) or MTY1Box(OUT)
			company=self.get_company(layout,layout_count)
			lpn = self.get_license_plate_number(layout,layout_count)
			

			contain1_no = self.get_container1(layout,layout_count)
			contain1_loc =  self.get_location1(layout,layout_count)
			contain1_seal = self.get_seal_number1(layout,layout_count)

			contain2_no = self.get_container2(layout,layout_count)
			contain2_loc =  self.get_location2(layout,layout_count)
			contain2_seal = self.get_seal_number2(layout,layout_count)


			call_card = self.get_call_card(layout,layout_count)
			time_stamp =self.get_timestamp(layout,layout_count)

			data = {
					'filename' : self.filename,
					'type' : layout_count,
					'company' : company ,
					'license_no': lpn,
					'call_card':call_card,
					'time_stamp' : time_stamp
					}



			if layout_count == 9 :
				# print("Full (IN)/Empty(Out) 1 Box TID")
				c2_text = self.get_line_text(layout,2)

				if len(c2_text) > 1 :
					direction='in'
					# print ('Full (IN) 1 box')
				else:
					direction='out'
					# print ('Full (OUT) 1 box')

				if direction=='in':
					data[direction]={}
					data[direction]['item1']={'container_no' : contain1_no,
								'location' : contain1_loc,
								'seal' : contain1_seal}

				if direction=='out':
					# either 1 or 2 Full out
					c4_text = self.get_line_text(layout,4)
					y= c4_text.split('  ')
					data[direction]={}
					if '-' in c4_text :
						data[direction]['item1']={'container_no' : contain1_no,
								'location' : contain1_loc,
								'seal' : contain1_seal,
								'line3':''}
					else:
						data[direction]['item1']={'container_no' : contain1_no,
								'location' : contain1_loc,
								'seal' : contain1_seal,
								'line3' : ''}
						data[direction]['item2']={'container_no' : contain2_no,
								'location' : contain2_loc,
								'seal' : contain2_seal,
								'line3' : ''}


					# data[direction]['item1']={'container_no' : contain1_no,
					# 			'location' : contain1_loc,
					# 			'seal' : contain1_seal}
				
			if layout_count == 7 :
				data['in']={}
				data['in']['item1']={'container_no' : contain1_no,
							'location' : contain1_loc,
							'seal' : contain1_seal}

				if self.get_line_text(layout,3) == '-' :
					data['in']['item2']={'container_no' : contain2_no,
					'location' : contain2_loc,
					'seal' : contain2_seal}
				else:
					data['out']={}
					data['out']['item1'] ={'container_no':'',
						'location' : '',
						'seal':''}
						# print('')



			if layout_count == 10 :
				data['in']={}
				data['in']['item1']={'container_no' : contain1_no,
							'location' : contain1_loc,
							'seal' : contain1_seal}


				tmp=self.get_line3text1(layout,layout_count)
				if rex.match(tmp):
					location=tmp
				else:
					location=''

				data['out']={}
				data['out']['item1']={
							'container_no' : self.get_service1(layout,layout_count),
							'seal' : self.get_container1_type(layout,layout_count),
							'line3' : self.get_line3text1(layout,layout_count),
							'location' : location}

				tmp=self.get_line3text2(layout,layout_count)
				if rex.match(tmp):
					location=tmp
				else:
					location=''

				data['out']['item2']={
							'container_no' : self.get_service2(layout,layout_count),
							'seal' : self.get_container2_type(layout,layout_count),
							'line3' : self.get_line3text2(layout,layout_count),
							'location' : location}

			if layout_count == 11 :
				data['out']={}
				tmp=self.get_line3text1(layout,layout_count)
				if rex.match(tmp):
					location=tmp
				else:
					location=''

				data['out']['item1']={
				'container_no' : self.get_service1(layout,layout_count),
				'seal' : self.get_container1_type(layout,layout_count),
				'line3' : self.get_line3text1(layout,layout_count),
				'location' : location
				}

				if self.get_line_text(layout,3)=='-' :
					tmp=self.get_line3text2(layout,layout_count)
					if rex.match(tmp):
						location=tmp
					else:
						location=''

					data['out']['item2']={
								'container_no' : self.get_service2(layout,layout_count),
								'seal' : self.get_container2_type(layout,layout_count),
								'line3' : self.get_line3text2(layout,layout_count),
								'location' : location}


			if layout_count == 12 :
				data['out']={}
				tmp=self.get_line3text1(layout,layout_count)
				if rex.match(tmp):
					location=tmp
				else:
					location=''

				data['out']['item1']={
							'container_no' : self.get_service1(layout,layout_count),
							'seal' : self.get_container1_type(layout,layout_count),
							'line3' : self.get_line3text1(layout,layout_count),
							'location' :location}

				tmp=self.get_line3text2(layout,layout_count)
				if rex.match(tmp):
					location=tmp
				else :
					location=''

				data['out']['item2']={
							'container_no' : self.get_service2(layout,layout_count),
							'seal' : self.get_container2_type(layout,layout_count),
							'line3' : self.get_line3text2(layout,layout_count),
							'location' :location}


			return data
				# For View file details
			# if argv[1] == 'y':
			   #  for lt_obj in layout:
			   #      if isinstance(lt_obj, LTTextBox) :
			   #      	line_text=lt_obj.get_text()

			   #      	print('%s) %s' % (i,line_text))
			   #      	i=i+1


			# print('-------------End Page----------------------------------------------')
	
	def getRaw(self):
		fp = open(self.filename, 'rb')
		parser = PDFParser(fp)
		doc = PDFDocument()
		parser.set_document(doc)
		doc.set_parser(parser)
		doc.initialize('')
		rsrcmgr = PDFResourceManager()
		laparams = LAParams()
		device = PDFPageAggregator(rsrcmgr, laparams=laparams)
		interpreter = PDFPageInterpreter(rsrcmgr, device)
		# Process each page contained in the document.
		images_folder=""
		text_content = []
		# print ("Info")
		import re
		rex = re.compile("^[0-9]{2}[A-Z][0-9]{2}[A-Z][0-9]$")
		i=0
		for page in doc.get_pages():
			interpreter.process_page(page)
			layout = device.get_result()
			for lt_obj in layout:
				if isinstance(lt_obj, LTTextBox) :
					line_text=lt_obj.get_text()
					print('%s) %s' % (i,line_text))
					i=i+1

	# tid_type 
	# 9 : Full(in) 1 box OR Empty(out) 1 box
	# 7 : Full(in) 2 box
	#12 : Empty(out) 2 box
	def get_company(self,layout,tid_type):
		line_text = self.get_line_text(layout,1)
		x = line_text.split('    ')
		return x[0].strip()
		# if tid_type == 9 or tid_type == 7 :
		# 	return x[0].strip()

		# if tid_type == 12 :
		# 	return x[0].strip()

	def get_license_plate_number(self,layout,tid_type):
		if tid_type == 9 or tid_type == 7 or tid_type == 10:
			line_text = self.get_line_text(layout,1)
			x = line_text.split('    ')
			return x[len(x)-1].strip().replace(' ','')


		if tid_type == 11 :
			line_text = self.get_line_text(layout,3) #Check 
			if line_text == '-':
				line_text = self.get_line_text(layout,1)
				x = line_text.split('    ')
				return x[len(x)-1].strip().replace(' ','')
			else:
				line_text = self.get_line_text(layout,2)
				return line_text.strip().replace(' ','')



		if tid_type == 12 :
			line_text = self.get_line_text(layout,2)
			x = line_text.split('    ')
			return x[0].strip().replace(' ','')

	def get_container1(self,layout,tid_type):
		if tid_type == 9 or tid_type == 7 :
			line_text = self.get_line_text(layout,2).strip()
			# print (line_text)
			if len(line_text) == 1:
				# return self.get_line_text(layout,4).strip(x = line_text.split('    ')).replace(' ','').replace('-','')
				line_text = self.get_line_text(layout,4).strip()
				x = line_text.split('    ')
				return x[0].strip().replace(' ','')
			else:
				x = line_text.split('    ')
				return x[0].strip().replace(' ','')

		if tid_type == 10 :
			line_text = self.get_line_text(layout,3).strip()
			x = line_text.split('    ')
			return x[0].strip().replace(' ','')


	def get_container2(self,layout,tid_type):
		if tid_type == 7 :
			line_text = self.get_line_text(layout,2).strip()
			x = line_text.split('    ')
			return x[1].strip().replace(' ','')

		if tid_type == 9 :
			line_text = self.get_line_text(layout,4).strip()
			x = line_text.split('    ')
			return x[len(x)-1].strip().replace(' ','')


	def get_location1(self,layout,tid_type):
		if tid_type == 7 : #Full(in)2 boxes
			line_text = self.get_line_text(layout,4).strip()
			x = line_text.split('    ')
			return x[0].strip().replace(' ','')

		if tid_type == 10 : 
			line_text = self.get_line_text(layout,7).strip()
			x = line_text.split('    ')
			return x[0].strip().replace(' ','')

		if tid_type == 9 :
			line_text = self.get_line_text(layout,5).strip()
			if len(line_text) > 1 :
				
				return line_text.strip().replace(' ','').replace('-','')
			else :
				line_text = self.get_line_text(layout,7).strip()
				x = line_text.split('    ')
				return x[0].strip().replace(' ','').replace('-','')
				# return self.get_line_text(layout,7).strip().replace(' ','').replace('-','')
			# print (line_text)
			# if len(line_text) == 1:
			# 	return get_line_text(layout,4).strip().replace(' ','').replace('-','')
			# else:
				
			# 	return x[0].strip().replace(' ','')

	def get_location2(self,layout,tid_type):
		if tid_type == 7 : #Full(in)2 boxes
			line_text = self.get_line_text(layout,4).strip()
			x = line_text.split('    ')
			return x[2].strip().replace(' ','')

		if tid_type == 9 : #Full(out)2 boxes
			line_text = self.get_line_text(layout,7).strip()
			x = line_text.split('    ')
			return x[len(x)-1].strip().replace(' ','')


	def get_seal_number1(self,layout,tid_type):
		if tid_type == 9 or tid_type == 7 :
			line_text = self.get_line_text(layout,6).strip()
			# print (line_text)
			if len(line_text) == 1:
				#1 Full Box IN
				# return self.get_line_text(layout,8).strip().replace(' ','').replace('-','')
				line_text = self.get_line_text(layout,8).strip()
				x = line_text.split('    ')
				return x[0].strip().replace(' ','').replace('-','')
			else:
				#2 Full boxes IN
				x = line_text.split('    ')
				return x[0].strip().replace(' ','').replace('-','')

		if tid_type == 10 :
			line_text = self.get_line_text(layout,9).strip()
			x = line_text.split('    ')
			return x[0].strip().replace(' ','').replace('-','')


	def get_seal_number2(self,layout,tid_type):
		if tid_type == 7 :
			line_text = self.get_line_text(layout,6).strip()
			#2 Full boxes IN
			x = line_text.split('    ')
			return x[1].strip().replace(' ','').replace('-','')

		if tid_type == 9 : #Full(out)2 boxes
			line_text = self.get_line_text(layout,8).strip()
			x = line_text.split('    ')
			return x[len(x)-1].strip().replace(' ','')
		

	def get_call_card(self,layout,tid_type):
		if tid_type == 9 or tid_type == 7 :
			line_text = self.get_line_text(layout,9).strip()
			# print (line_text)
			if len(line_text) == 0:
				#1 Full Box IN
				line_text=self.get_line_text(layout,7).strip()
				x = line_text.split('    ')
				return x[0].strip().replace(' ','').replace('-','')
			else:
				#2 Full boxes IN
				x = line_text.split('    ')
				return x[0].strip().replace(' ','').replace('-','')

		if tid_type == 10 :
			line_text = self.get_line_text(layout,10).strip()
			x = line_text.split('    ')
			return x[0].strip().replace(' ','').replace('-','')
		if tid_type == 11 :
			line_text = self.get_line_text(layout,11).strip()
			x = line_text.split('    ')
			return x[0].strip().replace(' ','').replace('-','')
		if tid_type == 12 :
			line_text = self.get_line_text(layout,12).strip()
			x = line_text.split('    ')
			return x[0].strip().replace(' ','').replace('-','')

	def get_timestamp(self,layout,tid_type):
		if tid_type == 9 or tid_type == 7 :
			line_text = self.get_line_text(layout,9).strip()
			# print (line_text)
			if len(line_text) == 0:
				#1 Full Box IN
				line_text=self.get_line_text(layout,7).strip()
				x = line_text.split('    ')
				# print (len(x))
				return x[len(x)-1].strip().replace('-','')
			else:
				#2 Full boxes IN
				x = line_text.split('    ')
				# print (len(x))
				return x[len(x)-1].strip().replace('-','')

		if tid_type == 10 :
			line_text = self.get_line_text(layout,10).strip()
			x = line_text.split('    ')
			return x[len(x)-1].strip().replace('-','')

		if tid_type == 11 :
			line_text = self.get_line_text(layout,11).strip()
			x = line_text.split('    ')
			return x[len(x)-1].strip().replace(' ','').replace('-','')
		if tid_type == 12 :
			line_text = self.get_line_text(layout,12).strip()
			x = line_text.split('    ')
			return x[len(x)-1].strip().replace(' ','').replace('-','')

			
	def get_service1(self,layout,tid_type):
		if tid_type == 10 :
			line_text = self.get_line_text(layout,2).strip()
			x = line_text.split('    ')
			return x[0].strip().replace(' ','')

		if tid_type == 11 :
			line_text = self.get_line_text(layout,3).strip()
			if line_text=='-':
				line_text = self.get_line_text(layout,2).strip()
				x = line_text.split('    ')
				return x[0].strip().replace(' ','')
			else:
				line_text = self.get_line_text(layout,3).strip()
				return line_text.strip().replace(' ','')


		if tid_type == 12 :
			line_text = self.get_line_text(layout,3).strip()
			x = line_text.split('    ')
			return x[0].strip().replace(' ','')

	def get_service2(self,layout,tid_type):

		if tid_type == 10 or tid_type == 11 :
			line_text = self.get_line_text(layout,2).strip()
			x = line_text.split('    ')
			return x[len(x)-1].strip().replace(' ','')

		if tid_type == 12 :
			line_text = self.get_line_text(layout,3).strip()
			x = line_text.split('    ')
			return x[len(x)-1].strip().replace(' ','')

	def get_container1_type(self,layout,tid_type):
		if tid_type == 10 :
			line_text1 = self.get_line_text(layout,4).strip()
			x = line_text1.split('    ')
			line_text2 = self.get_line_text(layout,5).strip()
			y = line_text2.split('    ')
			return '%s  %s' % (x[0].strip().replace(' ',''),y[0].strip().replace(' ','').replace('DV',' DV '))

		if tid_type == 11 :
			line_text = self.get_line_text(layout,3).strip()
			if line_text=='-':
				line_text1 = self.get_line_text(layout,5).strip()
				x = line_text1.split('    ')
				line_text2 = self.get_line_text(layout,6).strip()
				y = line_text2.split('    ')
				return '%s  %s' % (x[0].strip().replace(' ',''),y[0].strip().replace(' ','').replace('DV',' DV '))
			else:
				line_text1 = self.get_line_text(layout,6).strip()
				x = line_text1.split('    ')
				line_text2 = self.get_line_text(layout,7).strip()
				y = line_text2.split('    ')
				return '%s  %s' % (x[0].strip().replace(' ',''),y[0].strip().replace(' ','').replace('DV',' DV '))


		if tid_type == 12 :
			line_text1 = self.get_line_text(layout,6).strip()
			x = line_text1.split('    ')
			line_text2 = self.get_line_text(layout,7).strip()
			y = line_text2.split('    ')
			return '%s  %s' % (x[0].strip().replace(' ',''),y[0].strip().replace(' ','').replace('DV',' DV '))


	def get_container2_type(self,layout,tid_type):
		if tid_type == 10 :
			line_text1 = self.get_line_text(layout,5).strip()
			x = line_text1.split('    ')
			line_text2 = self.get_line_text(layout,6).strip()
			y = line_text2.split('    ')
			return '%s  %s' % (x[len(x)-1].strip().replace(' ',''),y[0].strip().replace(' ','').replace('DV',' DV '))

		if tid_type == 11 :
			line_text1 = self.get_line_text(layout,6).strip()
			x = line_text1.split('    ')
			line_text2 = self.get_line_text(layout,7).strip()
			y = line_text2.split('    ')
			return '%s  %s' % (x[len(x)-1].strip().replace(' ',''),y[0].strip().replace(' ','').replace('DV',' DV '))

		if tid_type == 12 :
			line_text1 = self.get_line_text(layout,7).strip()
			x = line_text1.split('    ')
			line_text2 = self.get_line_text(layout,8).strip()
			y = line_text2.split('    ')
			return '%s  %s' % (x[len(x)-1].strip().replace(' ',''),y[0].strip().replace(' ','').replace('DV',' DV '))

	def get_line3text1(self,layout,tid_type):
		if tid_type == 10 :
			line_text1 = self.get_line_text(layout,8).strip()
			x = line_text1.split('    ')
			return '%s' % (x[0].strip().replace(' ',''))

		if tid_type == 11 :
			line_text1 = self.get_line_text(layout,10).strip()
			x = line_text1.split('    ')
			return '%s' % (x[0].strip().replace(' ',''))

		if tid_type == 12 :
			line_text1 = self.get_line_text(layout,11).strip()
			x = line_text1.split('    ')
			return '%s' % (x[0].strip().replace(' ',''))

	def get_line3text2(self,layout,tid_type):
		if tid_type == 10 :
			line_text1 = self.get_line_text(layout,8).strip()
			x = line_text1.split('    ')
			return '%s' % (x[len(x)-1].strip().replace(' ',''))

		if tid_type == 11 :
			line_text1 = self.get_line_text(layout,10).strip()
			x = line_text1.split('    ')
			return '%s' % (x[len(x)-1].strip().replace(' ',''))

		if tid_type == 12 :
			line_text1 = self.get_line_text(layout,11).strip()
			x = line_text1.split('    ')
			return '%s' % (x[len(x)-1].strip().replace(' ',''))


	def _parse_pages (doc, images_folder):
		"""With an open PDFDocument object, get the pages, parse each one, and return the entire text
		[this is a higher-order function to be passed to with_pdf()]"""
		rsrcmgr = PDFResourceManager()
		laparams = LAParams()
		device = PDFPageAggregator(rsrcmgr, laparams=laparams)
		interpreter = PDFPageInterpreter(rsrcmgr, device)

		text_content = [] # a list of strings, each representing text collected from each page of the doc
		for i, page in enumerate(doc.get_pages()):
			interpreter.process_page(page)
			# receive the LTPage object for this page
			layout = device.get_result()
			# layout is an LTPage object which may contain child objects like LTTextBox, LTFigure, LTImage, etc.
			text_content.append(parse_lt_objs(layout.objs, (i+1), images_folder))

		return text_content

	def parse_lt_objs (lt_objs, page_number, images_folder, text=[]):
		"""Iterate through the list of LT* objects and capture the text or image data contained in each"""
		text_content = [] 

		for lt_obj in lt_objs:
			if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
				# text
				text_content.append(lt_obj.get_text())
				print(lt_obj.get_text())
			elif isinstance(lt_obj, LTImage):
				# an image, so save it to the designated folder, and note it's place in the text 
				saved_file = save_image(lt_obj, page_number, images_folder)
				if saved_file:
					# use html style <img /> tag to mark the position of the image within the text
					text_content.append('<img src="'+os.path.join(images_folder, saved_file)+'" />')
				else:
					print >> sys.stderr, "Error saving image on page", page_number, lt_obj.__repr__
			elif isinstance(lt_obj, LTFigure):
				# LTFigure objects are containers for other LT* objects, so recurse through the children
				text_content.append(parse_lt_objs(lt_obj.objs, page_number, images_folder, text_content))

		return text_content
		# return '\n'.join(text_content)

	# if __name__ == "__main__":
	#     sys.exit(main(sys.argv[1:]))

