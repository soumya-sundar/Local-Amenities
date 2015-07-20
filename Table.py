import logging
import os
import csv, codecs, cStringIO
import cloudstorage as gcs
import webapp2
import string
from models import *
from google.appengine.ext import db
from google.appengine.api import app_identity

class MainPage(webapp2.RequestHandler):
	def get(self):
		bucket_name = os.environ.get('local-amenities.appspot.com', app_identity.get_default_gcs_bucket_name())
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.write('Demo GCS Application running from Version: '
                        + os.environ['CURRENT_VERSION_ID'] + '\n')
		self.response.write('Using bucket name: ' + bucket_name + '\n\n')
		bucket = '/' + bucket_name
		#filename1 = bucket + '/GP.csv'
		#filename2 = bucket + '/Outcodes.csv'
		#filename3 = bucket + '/Postcodes.csv'
		#filename4 = bucket + '/TrainStation.csv'
		#filename5 = bucket + '/Supermarket.csv'
		filename6 = bucket + '/School.csv'

		#self.response.write('\n\nGeneral Practioners\n\n')
		#self.AccessGP(filename1)
		#self.response.write('\n\nOutcodes\n\n')
		#self.AccessOutcodes(filename2)
		#self.response.write('\n\nPostcodes\n\n')
		#self.AccessPostcodes(filename3)
		#self.response.write('\n\nTrain Station\n\n')
		#self.AccessTrainStation(filename4)
		#self.response.write('\n\nSupermarket\n\n')
		#self.AccessSupermarket(filename5)
		self.response.write('\n\nSchool\n\n')
		self.AccessSchool(filename6)

	def AccessGP(self,filename1):
		try:
			gp_list = []
			gcs_file=gcs.open(filename1)
			reader=csv.DictReader(gcs_file)
			for row in reader:
				if len(row['Latitude']) != 0:
					lat = float(row['Latitude'])
				else:
					lat = 0.00
				if len(row['Longitude']) != 0:
					long= float(row['Longitude'])
				else:
					long = 0.00
				coord = {'latitude': lat, 'longitude': long}	
				point = '{latitude}, {longitude}'.format(**coord)
				name = row['Name']
				postcode = row['Postcode'].replace(' ','')
				address = row['Address Line 1'] + ", " + row['Address Line 2'] + ", " + row['Address Line 3'] + ", " + row['Address Line 4'] + ", " + row['Address Line 5']
				gp = GP(name=unicode(name, "utf-8"),
						address=unicode(address, "utf-8"),
						postcode=unicode(postcode, "utf-8"),
						lat_long = point)
				gp_list.append(gp)
			db.put(gp_list)
			gcs_file.close()

		except Exception, e:  # pylint: disable=broad-except
			logging.exception(e)
			self.response.write('\n\nThere was an error running the demo! '
								'Please check the logs for more details.\n')

	def AccessOutcodes(self,filename2):
		try:
			outcode_list = []
			gcs_file=gcs.open(filename2)
			reader=csv.DictReader(gcs_file)
			for row in reader:
				code= row['outcode'].replace(' ','')
				if len(row['latitude']) != 0:
					lat = float(row['latitude'])
				else:
					lat = 0.00
				if len(row['longitude']) != 0:
					long= float(row['longitude'])
				else:
					long = 0.00
				coord = {'latitude': lat, 'longitude': long}	
				point = '{latitude}, {longitude}'.format(**coord)
				outcode = Outcode(outcode=code,
								  lat_long = point)
				outcode_list.append(outcode)
			db.put(outcode_list)
			gcs_file.close()

		except Exception, e:  # pylint: disable=broad-except
			logging.exception(e)
			self.response.write('\n\nThere was an error running the demo! '
								'Please check the logs for more details.\n')
								
	def AccessPostcodes(self, filename3):
		try:
			postcode_list =  []
			gcs_file=gcs.open(filename3)
			reader=csv.DictReader(gcs_file)
			for row in reader:
				code = row['postcode'].replace(' ','')
				if len(row['latitude']) != 0:
					lat = float(row['latitude'])
				else:
					lat = 0.00
				if len(row['longitude']) != 0:
					long= float(row['longitude'])
				else:
					long = 0.00
				coord = {'latitude': lat, 'longitude': long}	
				point = '{latitude}, {longitude}'.format(**coord)
				postcode = Postcode(postcode=code,
								    lat_long = point)
				postcode_list.append(postcode)
			gcs_file.close()

			self.batchPut(postcode_list, 10000)
			
		except Exception, e:  # pylint: disable=broad-except
			logging.exception(e)
			self.response.write('\n\nThere was an error running the demo! '
								'Please check the logs for more details.\n')
								
	def AccessTrainStation(self,filename4):
		try:
			train_list = []
			gcs_file=gcs.open(filename4)
			reader=csv.DictReader(gcs_file)
			for row in reader:
				if len(row['Latitude']) != 0:
					lat = float(row['Latitude'])
				else:
					lat = 0.00
				if len(row['Longitude']) != 0:
					long= float(row['Longitude'])
				else:
					long = 0.00
				coord = {'latitude': lat, 'longitude': long}	
				point = '{latitude}, {longitude}'.format(**coord)
				trainStation = TrainStation(name=row['StationName'],
											lat_long = point)				
				train_list.append(trainStation)
			db.put(train_list)
			gcs_file.close()

		except Exception, e:  # pylint: disable=broad-except
			logging.exception(e)
			self.response.write('\n\nThere was an error running the demo! '
								'Please check the logs for more details.\n')
								
	def AccessSupermarket(self,filename5):
		try:
			Supermarket_list = []
			gcs_file=gcs.open(filename5)
			reader=csv.DictReader(gcs_file)
			for row in reader:
				if len(row['Latitude']) != 0:
					lat = float(row['Latitude'])
				else:
					lat = 0.00
				if len(row['Longitude']) != 0:
					long= float(row['Longitude'])
				else:
					long = 0.00
				coord = {'latitude': lat, 'longitude': long}	
				point = '{latitude}, {longitude}'.format(**coord)
				name = row['StoreName']
				postcode = row['Postcode'].replace(' ','')
				address = row['Add1'] + ", " + row['Add2'] + ", " + row['Town'] + ", " + row['Locality']
				sp = Supermarket(name = unicode(name, "utf-8"),
								 address = unicode(address, "utf-8"),
								 postcode = unicode(postcode, "utf-8"),
								 lat_long = point)
				Supermarket_list.append(sp)
			db.put(Supermarket_list)
			gcs_file.close()

		except Exception, e:  # pylint: disable=broad-except
			logging.exception(e)
			self.response.write('\n\nThere was an error running the demo! '
								'Please check the logs for more details.\n')

	def AccessSchool(self,filename6):
		try:
			School_list = []
			gcs_file=gcs.open(filename6)
			reader=csv.DictReader(gcs_file)
			for row in reader:
				if len(row['Latitude']) != 0:
					lat = float(row['Latitude'])
				else:
					lat = 0.00
				if len(row['Longitude']) != 0:
					long= float(row['Longitude'])
				else:
					long = 0.00
				coord = {'latitude': lat, 'longitude': long}	
				point = '{latitude}, {longitude}'.format(**coord)
				name = row['EstablishmentName']
				postcode = row['Postcode'].replace(' ','')
				address = row['Street'] + ", " + row['Locality'] + ", " + row['Address3'] + ", " + row['Town'] + ", " + row['County (name)']
				school = School(name = unicode(name, "utf-8"),
								 address = unicode(address, "utf-8"),
								 postcode = unicode(postcode, "utf-8"),
								 lat_long = point)
				School_list.append(school)
			db.put(School_list)
			gcs_file.close()

		except Exception, e:  # pylint: disable=broad-except
			logging.exception(e)
			self.response.write('\n\nThere was an error running the demo! '
								'Please check the logs for more details.\n')

	def batchPut(self, entityList, batchSize=10000):
		putList = []
		count = len(entityList)
		while count > 0:
			batchSize = min(count,batchSize)
			putList = entityList[:batchSize]
			try:
				db.put(putList)
				entityList = entityList[batchSize:]
				count = len(entityList)
			except TooManyError,TooLargeError:
				batchSize = batchSize/2

app = webapp2.WSGIApplication([('/', MainPage)],
                              debug=True)