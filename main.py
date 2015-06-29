import logging
import os
import csv
import cloudstorage as gcs
import webapp2
import jinja2
import urllib

from google.appengine.api import app_identity
from google.appengine.api import users
from google.appengine.ext.webapp.util import login_required

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

#Handles application routes
app = webapp2.WSGIApplication([
    ('/', MainPage),
	('/search', NewSearch)
], debug=True)
	