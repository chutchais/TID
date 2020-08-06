import sys,getopt
import re

class tid:
	def __init__(self, filename):
		self.filename = filename
		self.container1_exist = False
		self.container2_exist = False
		self.container3_exist = False
		self.container4_exist = False
		self.MTY_exist =False
		self.container_line_number = 0

	# @staticmethod	

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

	def get_line_string_raw(self,line_no,start_pos):
		return self.text_content[line_no]

	def getInfo(self):
		self.text_content = []
		with open(self.filename) as f:
			self.text_content = f.readlines()
			# print (self.text_content)

		self.first_line_data = 0
		for l in self.text_content:
			if len(l[9:].strip())>1:
				break
			self.first_line_data = self.first_line_data+1



		company=self.get_company()
		lpn = self.get_license_plate_number()
		# container = self.get_container()
		# location = self.get_location()
		# seal = self.get_seal()
		
		call_card = self.get_call_card()
		time_stamp =self.get_timestamp()

		print ('%s--%s--%s--%s' % (company,lpn,call_card,time_stamp))

		
		c=self.get_service()
		container1,container2,container3,container4 = self.get_container()

		if len(container1)>1:
			self.container1_exist = True

		if len(container2)>1:
			self.container2_exist = True

		if len(container3)>1:
			self.container3_exist = True

		if len(container4)>1:
			self.container4_exist = True


		location1,location2,location3,location4 = self.get_location()
		seal1,seal2,seal3,seal4 = self.get_seal()

		seal2_1,seal2_2,seal2_3,seal2_4= self.get_seal2()
		print ('Seal2 %s' % seal2_1)

# Add by Chutchai S on Oct 30,2018
# To get Damage message
		damage3,damage4,damage1,damage2= self.get_damage()
		print ('Damage %s %s' % (damage3,damage4))
# finished
		import re
		rex = re.compile("^[0-9]{2}[A-Z][0-9]{2}[A-Z][0-9]$")

		line3_3=''
		line3_4=''

		# if self.container3_exist and self.container4_exist :
		if self.MTY_exist :
			print ('Both Empty out')
			line_number = self.container_line_number
			line_text1 = self.get_line_string(line_number,1)
			a = self.split_data(line_text1)
			print (a)
			
			location3_tmp = location3
			location4_tmp = location4

			# if rex.match(seal3):
			# 	location3 =seal3
			# else:
			# 	location3=''

			# if rex.match(seal4):
			# 	location4 =seal4
			# else:
			# 	location4=''

			line3_3 = seal3
			line3_4 = seal4

			seal3=a[2]
			seal4=a[3]

		# data = {
		# 		'company': company,
		# 	    'containers': [
		# 	        {
		# 	            'number': container1,
		# 	            'position': self.convert_location(location1),
		# 	            'seal1': seal1.replace('L SL ',''),
		# 	            'seal2': seal2_1.replace('L SL ',''),
		# 	            'trans_type': 'RE',
		# 	            'damage': damage1,
		# 	        },
		# 	        {
		# 	            'number': container2,
		# 	            'position': self.convert_location(location2),
		# 	            'seal1': seal2.replace('L SL ',''),
		# 	            'seal2': seal2_2.replace('L SL ',''),
		# 	            'trans_type': 'RE',
		# 	            'damage': damage2,
		# 	        },
		# 	        {
		# 	            'number': container3,
		# 	            'position': self.convert_location(location3),
		# 	            'seal1': seal3.replace('L SL ',''),
		# 	            'seal2': line3_3.replace('L SL ',''),
		# 	            'trans_type': 'DI',
		# 	            'damage': damage3,
		# 	        },
		# 	        {
		# 	            'number': container4,
		# 	            'position': self.convert_location(location4),
		# 	            'seal1': seal4.replace('L SL ',''),
		# 	            'seal2': line3_4.replace('L SL ',''),
		# 	            'trans_type': 'DI',
		# 	            'damage': damage4,
		# 	        }
		# 	    ],
		# 	    'document': 'TID',
		# 	    'license': call_card,
		# 	    'printer' : 'EPSON TM-T82',
		# 	    'start': time_stamp,
		# 	    'ttl': 3600
		# }
		data = {
		'company': company,
	    'containers': [],
	    'document': 'TID',
	    'license': call_card,
	    'printer' : 'EPSON TM-T82',
	    'start': time_stamp,
	    'ttl': 3600,
	    'note' : lpn
		}

		if self.container1_exist :
			data['containers'].append(
			      {
			            'number': container1,
			            'position': self.convert_location(location1),
			            'seal1': seal1.replace('L SL ',''),
			            'seal2': seal2_1.replace('L SL ',''),
			            'trans_type': 'RE',
			            'damage': damage1,
	        	})
		if self.container2_exist :
			data['containers'].append(
		        {
		            'number': container2,
		            'position': self.convert_location(location2),
		            'seal1': seal2.replace('L SL ',''),
		            'seal2': seal2_2.replace('L SL ',''),
		            'trans_type': 'RE',
		            'damage': damage2,
		        })
		if self.container3_exist :
			data['containers'].append(
		        {
		            'number': container3,
		            'position': self.convert_location(location3),
		            'seal1': seal3.replace('L SL ',''),
		            'seal2': line3_3.replace('L SL ',''),
		            'trans_type': 'DI',
		            'damage': damage3,
		        })
		if self.container4_exist :
			data['containers'].append(
		        {
		            'number': container4,
		            'position': self.convert_location(location4),
		            'seal1': seal4.replace('L SL ',''),
		            'seal2': line3_4.replace('L SL ',''),
		            'trans_type': 'DI',
		            'damage': damage4,
		        })
		# print(data)
		# data = {
		# 			'filename' : self.filename,
		# 			'first_line' : self.first_line_data,
		# 			'company' : company ,
		# 			'license_no': lpn,
		# 			'call_card':call_card,
		# 			'time_stamp' : time_stamp,
		# 			'in' : {
		# 					'item1':{
		# 						'container_no':container1,
		# 						'location':location1,
		# 						'seal':seal1,
		# 						'seal2':seal2_1,
		# 						'damage':damage1
		# 					},
		# 					'item2':{
		# 						'container_no':container2,
		# 						'location':location2,
		# 						'seal':seal2,
		# 						'seal2':seal2_2,
		# 						'damage':damage2
		# 					}

		# 				},
		# 			'out' : {
		# 					'item1':{
		# 						'container_no':container3,
		# 						'location':location3,
		# 						'seal':seal3,
		# 						'line3':line3_3,
		# 						'damage':damage3
		# 					},
		# 					'item2':{
		# 						'container_no':container4,
		# 						'location':location4,
		# 						'seal':seal4,
		# 						'line3':line3_4,
		# 						'damage':damage4
		# 					}

		# 				}
		# 			}
		# print(data)
		return data
	
	def getRaw(self):
		self.text_content = []
		with open(self.filename) as f:
			self.text_content = f.readlines()
		return self.text_content


	def get_company(self):
		line_number = self.first_line_data
		line_text = self.get_line_string(line_number,1)
		x=line_text.split('    ')
		return x[0].strip()


	def get_license_plate_number(self):
		line_number = self.first_line_data
		line_text = self.get_line_string(line_number,1)
		x=line_text.split('    ')
		return x[len(x)-1].strip()

	def get_call_card(self):
		line_text1 = self.get_line_string(len(self.text_content)-1,1)
		x=line_text1.split('    ')
		return x[0].strip()


	def get_timestamp(self):
		line_text1 = self.get_line_string(len(self.text_content)-1,1)
		x=line_text1.split('    ')
		return x[len(x)-1].strip()

	def get_service(self):
		line_number = self.first_line_data+1
		line_text1 = self.get_line_string(line_number,1)
		self.MTY_exist = False
		if len(line_text1) > 0 :
			# There are MTY out
			self.MTY_exist = True
			self.container_line_number = line_number+1
			line_text1 = self.get_line_string(line_number,1)
			print ('MTY exist %s' % line_text1)
		else :
			self.container_line_number = line_number+1



	def get_container(self):
		# a= '1','2','3','4'
		line_number = self.first_line_data+1
		line_service_text1 = self.get_line_string(line_number,1)
		s = self.split_data(line_service_text1)
		print (s)

		line_number = self.container_line_number
		# if self.MTY_exist :
		# self.container_line_number = line_number
		line_text1 = self.get_line_string(line_number,1)
		a = self.split_data(line_text1)
		print (a)

		if self.MTY_exist :
			# a[2]=s[0]
			# a[3]=s[1]
			b = a[0],a[1],s[0],s[1]
			return b

		return a




		# # Check Is it Empty out
		# if self.MTY_exist :
		# 	# assume they are empty box out
		# 	x=line_text1.split('    ')
		# 	data1=''
		# 	data2=''
		# 	data3=x[0]
		# 	data4=x[len(x)-1]
		# 	return data1,data2,data3,data4
		# else:
		# 	return self.split_data(line_text1)#line_text1.split('    ')

	def get_location(self):
		line_number = self.container_line_number+1
		line_text1 = self.get_line_string(line_number,1)
		self.location_line_number = line_number
		if len(line_text1) ==0 :
			line_text1 = self.get_line_string(line_number+1,1)
			self.location_line_number = line_number+1
		return self.split_data(line_text1)#line_text1.split('    ')

	def get_seal(self):
		line_number = self.location_line_number+1
		line_text1 = self.get_line_string(line_number,1)
		self.seal_line_number = line_number
		if len(line_text1) ==0 :
			line_text1 = self.get_line_string(line_number+1,1)
			self.seal_line_number = line_number+1

		# Check Is it Empty out
		data1=''
		data2=''
		data3=''
		data4=''
		x= self.split_data(line_text1) #line_text1.split('    ')
		print (x)
		print (len(x))

		if self.container1_exist :
			data1 = x[0]

		if self.container1_exist and self.container2_exist:
			data1 = x[0]
			data2 = x[1]

		if self.container3_exist:
			data3 = x[2]

		if self.container3_exist and (not self.container1_exist):
			data3 = x[0]

		if self.container3_exist and self.container4_exist and (not self.container1_exist):
			data3 = x[0]
			data4 = x[1]

		if self.container3_exist and self.container4_exist and x[0]=='-' and x[1]=='-' :
			data3 = x[2]
			data4 = x[3]



		return data1,data2,data3,data4

	def get_seal2(self):
		line_number = self.seal_line_number+1
		line_text1 = self.get_line_string(line_number,1)
		self.seal2_line_number = line_number
		print ('line %s' % line_number)
		return self.split_data(self.get_line_string(line_number,1))


# Add by Chutchai S on Oct 30,2018
# To get Damage message
	def get_damage(self):
		line_number = self.seal2_line_number+1
		line_text1 = self.get_line_string(line_number,1)
		# self.seal2_line_number = line_number
		print ('line of Damage: %s' % line_number)
		print (self.split_data(line_text1))
		return self.split_data(self.get_line_string(line_number,1))

		# if len(line_text1.split('-'))<2:
		# 	# assume they are empty box out
		# 	x=line_text1.split('    ')
		# 	data1=''
		# 	data2=''
		# 	data3=x[0]
		# 	data4=''
		# 	return data1,data2,data3,data4
		# else:
		# return self.split_data(line_text1)#line_text1.split('    ')

	def split_data(self,text_in):
		x= text_in.split('    ')
		data1=''
		data2=''
		data3=''
		data4=''
		i=0
		for d in x:
			if len(d.strip())>0:
				if i==0:
					data1= d.strip()
				if i==1:
					data2= d.strip()
				if i==2:
					data3= d.strip()
				if i==3:
					data4= d.strip()
				i=i+1
		return data1,data2,data3,data4



	

	


	

