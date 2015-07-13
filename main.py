import logging
import os
import csv
import cloudstorage as gcs
import webapp2
import jinja2
import json
import urllib
import logging
from math import radians, cos, sin, asin, sqrt
logging.getLogger().setLevel(logging.DEBUG)

from google.appengine.api import app_identity
from google.appengine.api import users
from google.appengine.ext.webapp.util import login_required
from array import *

AVG_EARTH_RADIUS = 6371  # in km

#set jinja2 environment to connect html with python
jinja_environment = jinja2.Environment(autoescape=True,
                                       loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),
                                                                                   'templates')))

#Render the main page of the application
class MainPage(webapp2.RequestHandler):
    def get(self):
        current_user = users.get_current_user()
        if current_user:
            url = users.create_logout_url(self.request.uri)
            url_text = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_text = 'Login'

        template_values = {
            'url': url,
            'url_text': url_text
        }
        # deal with static files
        template = jinja_environment.get_template('index.html')
        self.response.write(template.render(template_values))
		
#Render new search page
class NewSearch(webapp2.RequestHandler):
	@login_required
	def get(self):
		current_user = users.get_current_user().nickname()
		url = users.create_logout_url(self.request.uri)
		template_values = {'user_nickname': current_user, 'url': url}
		template = jinja_environment.get_template('search.html')
		self.response.write(template.render(template_values))
		
# Process entered postcode. 
class ProcessPostCode(webapp2.RequestHandler):
	def post(self):
		lat_long = []
		uPostcode = self.request.get('postcode').upper().strip()
		tPostcode = uPostcode.replace(' ','')
		logging.info(tPostcode)
		bucket_name = os.environ.get('local-amenities.appspot.com', app_identity.get_default_gcs_bucket_name())
		bucket = '/' + bucket_name
		filename1 = bucket + '/Outcodes.csv'
		filename2 = bucket + '/Postcodes.csv'
		filename3 = bucket + '/Postcodes2.csv'
		filename4 = bucket + '/Postcodes3.csv'
		filename5 = bucket + '/Postcodes4.csv'
		
		lat_long = self.AccessOutcodes(filename1, tPostcode)
		if(len(lat_long) == 0):
			lat_long = self.AccessPostcodes(filename2, tPostcode)
			if(len(lat_long) == 0):
				lat_long = self.AccessPostcodes2(filename3, tPostcode)
				if(len(lat_long) == 0):
					lat_long = self.AccessPostcodes3(filename4, tPostcode)
					if(len(lat_long) == 0):
						lat_long = self.AccessPostcodes4(filename5, tPostcode)
						if(len(lat_long) == 0):
							self.response.out.write(json.dumps({'found': False}))
							return

		self.response.out.write(json.dumps({'found': True, 'postcode': tPostcode, 'latitude': lat_long[0], 'longitude': lat_long[1]}))

	def AccessOutcodes(self, filename1, tPostcode):	
		lat_long_outcodes = []
		try:
			gcs_file=gcs.open(filename1)
			reader=csv.DictReader(gcs_file)
			for row in reader:
				if row['outcode'] == tPostcode:
					lat_long_outcodes.insert(0,row['latitude'])
					lat_long_outcodes.insert(1,row['longitude'])
					break
			gcs_file.close()
			return lat_long_outcodes

		except Exception, e: 
			logging.exception(e)
			self.response.write('\n\nThere was an error running the demo! '
								'Please check the logs for more details.\n')

	def AccessPostcodes(self, filename2, tPostcode):	
		lat_long_outcodes = []
		try:
			gcs_file=gcs.open(filename2)
			reader=csv.DictReader(gcs_file)
			for row in reader:
				if row['postcode'] == tPostcode:
					lat_long_outcodes.insert(0,row['latitude'])
					lat_long_outcodes.insert(1,row['longitude'])
					break
			gcs_file.close()
			return lat_long_outcodes

		except Exception, e: 
			logging.exception(e)
			self.response.write('\n\nThere was an error running the demo! '
								'Please check the logs for more details.\n')

	def AccessPostcodes2(self, filename3, tPostcode):	
		lat_long_outcodes = []
		try:
			gcs_file=gcs.open(filename3)
			reader=csv.DictReader(gcs_file)
			for row in reader:
				if row['postcode'] == tPostcode:
					lat_long_outcodes.insert(0,row['latitude'])
					lat_long_outcodes.insert(1,row['longitude'])
					break
			gcs_file.close()
			return lat_long_outcodes

		except Exception, e: 
			logging.exception(e)
			self.response.write('\n\nThere was an error running the demo! '
								'Please check the logs for more details.\n')

	def AccessPostcodes3(self, filename4, tPostcode):	
		lat_long_outcodes = []
		try:
			gcs_file=gcs.open(filename4)
			reader=csv.DictReader(gcs_file)
			for row in reader:
				if row['postcode'] == tPostcode:
					lat_long_outcodes.insert(0,row['latitude'])
					lat_long_outcodes.insert(1,row['longitude'])
					break
			gcs_file.close()
			return lat_long_outcodes

		except Exception, e: 
			logging.exception(e)
			self.response.write('\n\nThere was an error running the demo! '
								'Please check the logs for more details.\n')

	def AccessPostcodes4(self, filename5, tPostcode):	
		lat_long_outcodes = []
		try:
			gcs_file=gcs.open(filename5)
			reader=csv.DictReader(gcs_file)
			for row in reader:
				if row['postcode'] == tPostcode:
					lat_long_outcodes.insert(0,row['latitude'])
					lat_long_outcodes.insert(1,row['longitude'])
					break
			gcs_file.close()
			return lat_long_outcodes

		except Exception, e: 
			logging.exception(e)
			self.response.write('\n\nThere was an error running the demo! '
								'Please check the logs for more details.\n')

# Look up for nearest amenities. 
class lookUp(webapp2.RequestHandler):
	def post(self):
		gp = []
		postcode = self.request.get('postcode')
		latitude = self.request.get('latitude')
		longitude = self.request.get('longitude')
		logging.info(postcode)
		logging.info(latitude)
		logging.info(longitude)
		bucket_name = os.environ.get('local-amenities.appspot.com', app_identity.get_default_gcs_bucket_name())
		bucket = '/' + bucket_name
		GP_file = bucket + '/GP.csv'
		gp = self.AccessGP(GP_file, postcode, latitude, longitude)
		#logging.info(json.dumps(gp))		
		self.response.out.write(json.dumps(gp))
		
	def AccessGP(self, GP_file, postcode, latitude, longitude):
		try:
			gp =[]
			distance = 0
			gcs_file=gcs.open(GP_file)
			reader=csv.DictReader(gcs_file)
			for row in reader:
				if len(row['Latitude']) != 0 and len(row['Longitude']) != 0 :
					point1= (float(latitude), float(longitude))
					point2= (float(row['Latitude']), float(row['Longitude']))
					distance = self.haversine(point1, point2)
					#if distance <= 48.28 :
					name = row['Name']
					address = row['Address Line 1'] + " " + row['Address Line 2'] + " " + row['Address Line 3'] + " " + row['Address Line 4'] + " " + row['Address Line 5']
					postcode = row['Postcode']
					latitude = row['Latitude']
					longitude = row['Longitude']
					gp.append({'name': name, 'address' : address, 'postcode': postcode, 'latitude': latitude, 'longitude': longitude, 'distance': distance})
			gcs_file.close()
			return  gp

		except Exception, e: 
			logging.exception(e)
			self.response.write('\n\nThere was an error running the demo! '
								'Please check the logs for more details.\n')
								
	def haversine(self, point1, point2):
		# unpack latitude/longitude
		lat1, lng1 = point1
		lat2, lng2 = point2

		# convert all latitudes/longitudes from decimal degrees to radians
		lat1, lng1, lat2, lng2 = list(map(radians, [lat1, lng1, lat2, lng2]))

		# calculate haversine
		lat = lat2 - lat1
		lng = lng2 - lng1
		d = sin(lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(lng / 2) ** 2
		h = 2 * AVG_EARTH_RADIUS * asin(sqrt(d))
		return round(h * 0.621371, 2)  # in miles

#Handles application routes
app = webapp2.WSGIApplication([
    ('/', MainPage),
	('/search', NewSearch),
	('/processPostCode', ProcessPostCode),
	('/lookUp', lookUp)
], debug=True)
	