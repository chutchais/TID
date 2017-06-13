import sys,getopt

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

	def get_line_string(self,line_no,start_pos):
		return self.text_content[line_no].strip()

	def getInfo(self):
		self.text_content = []
		with open(self.filename) as f:
			self.text_content = f.readlines()

		self.first_line_data = 0
		for l in self.text_content:
			if len(l[9:].strip())>1:
				# print ('Data is %s' % l[9:].strip() )
				# print ('First line is %s' % self.first_line_data )
				break
			self.first_line_data = self.first_line_data+1
		# Initial
		self.in_container1_exist =False
		self.in_container2_exist =False
		self.out_container1_exist =False
		self.out_container2_exist =False

		company=self.get_company()
		lpn = self.get_license_plate_number()
		container1 = self.get_container1()
		container2 = self.get_container2()
		container3 = self.get_container3()
		container4 = self.get_container4()
		location1 = self.get_location1()
		location2 = self.get_location2()
		location3 = self.get_location3()
		location4 = self.get_location4()
		seal1 = self.get_seal1()
		seal2 = self.get_seal2()
		seal3 = self.get_seal3()
		seal4 = self.get_seal4()
		call_card = self.get_call_card()
		time_stamp =self.get_timestamp()

		print ('%s--%s--%s--%s' % (company,lpn,call_card,time_stamp))
		print ('%s--%s--%s' % (container1,location1,seal1))
		print ('%s--%s--%s' % (container2,location2,seal2))
		print ('%s--%s--%s' % (container3,location3,seal3))
		print ('%s--%s--%s' % (container4,location4,seal4))
		data = {
					'filename' : self.filename,
					'first_line' : self.first_line_data,
					'company' : company ,
					'license_no': lpn,
					'call_card':call_card,
					'time_stamp' : time_stamp,
					'in' : {
							'item1':{
								'container_no':container1,
								'location':location1,
								'seal':seal1
							},
							'item2':{
								'container_no':container2,
								'location':location2,
								'seal':seal2
							}

						},
					'out' : {
							'item1':{
								'container_no':container3,
								'location':location3,
								'seal':seal3,
								'line3':''
							},
							'item2':{
								'container_no':container4,
								'location':location4,
								'seal':seal4,
								'line3':''
							}

						}
					}
		return data
	

	def get_company(self):
		line_number = self.first_line_data
		line_text = self.get_line_string(line_number,1)
		return line_text


	def get_license_plate_number(self):
		line_number = self.first_line_data+1
		line_text = self.get_line_string(line_number,1)
		return line_text


	def get_container1(self):
		line_number =line_number = self.first_line_data+4
		line_text1 = self.get_line_string(line_number,1)
		if line_text1 == '-' :
			self.in_container1_exist = False 
			self.in_container1_line = line_number
			return '-'
		else:
			self.in_container1_exist = True
			self.in_container1_line = line_number
			line_text2 = self.get_line_string(line_number+1,1)
			line_text3 = self.get_line_string(line_number+2,1)
			return line_text1+line_text2+line_text3

	def get_container2(self):
		if self.in_container1_exist :
			line_number = self.in_container1_line+3
		else:
			line_number = self.in_container1_line+1

		line_text1 = self.get_line_string(line_number,1)
		self.in_container2_line = line_number
		if line_text1 == '-' :
			self.in_container2_exist = False
			return '-'
		else:
			self.in_container2_exist = True
			line_text2 = self.get_line_string(line_number+1,1)
			line_text3 = self.get_line_string(line_number+2,1)
			return line_text1+line_text2+line_text3

	def get_container3(self):
		if self.in_container2_exist :
			line_number = self.in_container2_line+3
		else:
			line_number = self.in_container2_line+1

		line_text1 = self.get_line_string(line_number,1)
		self.in_container3_line = line_number
		if line_text1 == '-' :
			self.in_container3_exist = False
			return '-'
		else:
			self.in_container3_exist = True
			line_text2 = self.get_line_string(line_number+1,1)
			line_text3 = self.get_line_string(line_number+2,1)
			return line_text1+line_text2+line_text3

	def get_container4(self):
		if self.in_container3_exist :
			line_number = self.in_container3_line+3
		else:
			line_number = self.in_container3_line+1

		line_text1 = self.get_line_string(line_number,1)
		self.in_container4_line = line_number
		if line_text1 == '-' :
			self.in_container4_exist = False
			return '-'
		else:
			self.in_container4_exist = True
			line_text2 = self.get_line_string(line_number+1,1)
			line_text3 = self.get_line_string(line_number+2,1)
			return line_text1+line_text2+line_text3


	def get_location1(self):
		if self.in_container4_exist:
			line_number = self.in_container4_line + 3 + 2
			# print (line_number)
		else :
			line_number = self.in_container4_line +  2
			# print (line_number)

		self.in_location_line1 = line_number
		line_text1 = self.get_line_string(line_number,1)
		return line_text1

	def get_location2(self):
		line_number = self.in_location_line1+1
		self.in_location_line2 = line_number
		line_text1 = self.get_line_string(line_number,1)
		return line_text1

	def get_location3(self):
		line_number = self.in_location_line2+1
		self.in_location_line3 = line_number
		line_text1 = self.get_line_string(line_number,1)
		return line_text1

	def get_location4(self):
		line_number = self.in_location_line3+1
		self.in_location_line4 = line_number
		line_text1 = self.get_line_string(line_number,1)
		return line_text1


	def get_seal1(self):
		line_number = self.in_location_line4 + 2
		self.in_seal_line1 = line_number
		if self.in_container1_exist :
			line_text1 = self.get_line_string(line_number+0,1)
			line_text2 = self.get_line_string(line_number+1,1)
			line_text3 = self.get_line_string(line_number+2,1)
			return line_text1+line_text2+line_text3
		else :
			return '-'

	def get_seal2(self):
		if self.in_container1_exist :
			line_number = self.in_seal_line1 +3
		else :
			line_number = self.in_seal_line1 +1
		self.in_seal_line2 = line_number
		if self.in_container2_exist :
			line_text1 = self.get_line_string(line_number+0,1)
			line_text2 = self.get_line_string(line_number+1,1)
			line_text3 = self.get_line_string(line_number+2,1)
			return line_text1+line_text2+line_text3
		else :
			return '-'

	def get_seal3(self):
		if not (self.in_container1_exist and self.in_container2_exist) :
			line_number = self.in_seal_line2 -1
		else :
			line_number = self.in_seal_line2 

		self.in_seal_line3 = line_number
		if self.in_container3_exist :
			line_text1 = self.get_line_string(line_number+0,1)
			line_text2 = self.get_line_string(line_number+1,1)
			line_text3 = self.get_line_string(line_number+2,1)
			return line_text1+line_text2+line_text3
		else :
			return '-'

	def get_seal4(self):
		if self.in_container3_exist :
			line_number = self.in_seal_line3 + 3
		else :
			line_number = self.in_seal_line3 +1 

		self.in_seal_line4 = line_number
		if self.in_container3_exist :
			line_text1 = self.get_line_string(line_number+0,1)
			line_text2 = self.get_line_string(line_number+1,1)
			line_text3 = self.get_line_string(line_number+2,1)
			return line_text1+line_text2+line_text3
		else :
			return '-'


	
	def get_call_card(self):
		line_text1 = self.get_line_string(len(self.text_content)-3,1)
		return line_text1


	def get_timestamp(self):
		line_text1 = self.get_line_string(len(self.text_content)-2,1)
		line_text2 = self.get_line_string(len(self.text_content)-1,1)
		return line_text1 + ' ' + line_text2

	

