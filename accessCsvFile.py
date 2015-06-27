import logging
import os
import csv
import cloudstorage as gcs
import webapp2
import string

from google.appengine.api import app_identity

class MainPage(webapp2.RequestHandler):
	"""Main page for GCS demo application."""

	def get(self):
		bucket_name = os.environ.get('local-amenities.appspot.com', app_identity.get_default_gcs_bucket_name())
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.write('Demo GCS Application running from Version: '
                        + os.environ['CURRENT_VERSION_ID'] + '\n')
		self.response.write('Using bucket name: ' + bucket_name + '\n\n')
		bucket = '/' + bucket_name
		filename1 = bucket + '/Supermarket.csv'
		filename2 = bucket + '/TrainStation.csv'
		filename3 = bucket + '/GP.csv'
		filename4 = bucket + '/School.csv'
		filename5 = bucket + '/School2.csv'
		self.tmp_filenames_to_clean_up = []
        
		self.response.write('Supermarkets located in Newbury\n\n')
		self.AccessSupermarket(filename1)
		self.response.write('\n\nTrain stations in Southampton\n\n')
		self.AccessTrainStation(filename2)
		self.response.write('\n\nGeneral Practioners in Reading\n\n')
		self.AccessGP(filename3)
		self.response.write('\n\nSchools in Alford\n\n')
		self.AccessSchool(filename4,filename5)
	
	def AccessSupermarket(self,filename1):
		try:
			gcs_file=gcs.open(filename1)
			reader=csv.DictReader(gcs_file)
			for row in reader:
				if row['Town'] == 'Newbury':
					self.response.write(row)
					self.response.write('\n')
			gcs_file.close()

		except Exception, e:  # pylint: disable=broad-except
			logging.exception(e)
			self.response.write('\n\nThere was an error running the demo! '
								'Please check the logs for more details.\n')
	
	def AccessTrainStation(self,filename2):
		try:
			gcs_file=gcs.open(filename2)
			reader=csv.DictReader(gcs_file)
			str1='Southampton'
			for row in reader:
				if (string.find(row['StationName'],str1) >=0) :
					self.response.write(row)
					self.response.write('\n')
			gcs_file.close()

		except Exception, e:  # pylint: disable=broad-except
			logging.exception(e)
			self.response.write('\n\nThere was an error running the demo! '
								'Please check the logs for more details.\n')

	def AccessGP(self,filename3):
		try:
			gcs_file=gcs.open(filename3)
			reader=csv.DictReader(gcs_file)
			str1='READING'
			for row in reader:
				if (string.find(row['Address Line 3'],str1) >=0) :
					self.response.write(row)
					self.response.write('\n')
			gcs_file.close()

		except Exception, e:  # pylint: disable=broad-except
			logging.exception(e)
			self.response.write('\n\nThere was an error running the demo! '
								'Please check the logs for more details.\n')

	def AccessSchool(self,filename4,filename5):
		try:
			gcs_file=gcs.open(filename4)
			reader=csv.DictReader(gcs_file)
			for row in reader:
				if row['Town'] == 'Alford' :
					self.response.write(row)
					self.response.write('\n')
			gcs_file.close()
			gcs_file2=gcs.open(filename5)
			reader=csv.DictReader(gcs_file2)
			for row in reader:
				if row['Town'] == 'Alford' :
					self.response.write(row)
					self.response.write('\n')
			gcs_file2.close()

		except Exception, e:  # pylint: disable=broad-except
			logging.exception(e)
			self.response.write('\n\nThere was an error running the demo! '
								'Please check the logs for more details.\n')

app = webapp2.WSGIApplication([('/', MainPage)],
                              debug=True)