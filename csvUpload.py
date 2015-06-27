import logging
import os
import csv
import cloudstorage as gcs
import webapp2

from google.appengine.api import app_identity

# Retry can help overcome transient urlfetch or GCS issues, such as timeouts.
my_default_retry_params = gcs.RetryParams(initial_delay=0.2,
                                          max_delay=5.0,
                                          backoff_factor=2,
                                          max_retry_period=15)
# All requests to GCS using the GCS client within current GAE request and
# current thread will use this retry params as default. If a default is not
# set via this mechanism, the library's built-in default will be used.
# Any GCS client function can also be given a more specific retry params
# that overrides the default.
# Note: the built-in default is good enough for most cases. We override
# retry_params here only for demo purposes.
gcs.set_default_retry_params(my_default_retry_params)


class MainPage(webapp2.RequestHandler):
	"""Main page for GCS demo application."""

	def get(self):
		bucket_name = os.environ.get('local-amenities.appspot.com', app_identity.get_default_gcs_bucket_name())
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.write('Demo GCS Application running from Version: '
                        + os.environ['CURRENT_VERSION_ID'] + '\n')
		self.response.write('Using bucket name: ' + bucket_name + '\n\n')
		bucket = '/' + bucket_name
		filename = bucket + '/School2.csv'
		self.tmp_filenames_to_clean_up = []
		
		try:
			self.create_file(filename)
			self.response.write('\n\n')
			self.read_file(filename)
			self.response.write('\n\n')

		except Exception, e:  # pylint: disable=broad-except
			logging.exception(e)
			self.response.write('\n\nThere was an error running the demo! '
								'Please check the logs for more details.\n')
 
# When writing a file to Cloud Storage, you should not call finally:close() as
# this can result in finalizing object uploads even if there was an exception
# during a write.
	def create_file(self, filename):
		self.response.write('Creating file %s\n' % filename)
		write_retry_params = gcs.RetryParams(backoff_factor=1.1)
		gcs_file = gcs.open(filename,
							'w',
							content_type='text/csv',
							retry_params=write_retry_params)
		f=open('School2.csv')
		reader=csv.reader(f)
		writer = csv.writer(gcs_file)
		for row in reader:        
			writer.writerow(row)
		gcs_file.close()
		self.tmp_filenames_to_clean_up.append(filename)

	def read_file(self, filename):
		self.response.write('Abbreviated file content (first line and last 1K):\n')
		gcs_file = gcs.open(filename)
		self.response.write(gcs_file.readline())
		gcs_file.seek(-1024, os.SEEK_END)
		self.response.write(gcs_file.read())
		gcs_file.close()

app = webapp2.WSGIApplication([('/', MainPage)],
                              debug=True)