import jinja2
import webapp2
import os
import json
import urllib
import urllib2
import datetime
from google.appengine.ext import ndb
from google.appengine.api import users

jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)))

class InfoPage(webapp2.RequestHandler):
    def get(self):
        info = jinja_env.get_template('templates/info.html')
        self.response.write(info.render())

class HomePage(webapp2.RequestHandler):
        def get(self):

            dateInfo = {
                "month": datetime.datetime.now().strftime("%A, %B %d, %Y")
            }

            home = jinja_env.get_template('templates/home.html')
            self.response.write(home.render(dateInfo))

app = webapp2.WSGIApplication([
    ('/', InfoPage),
    ('/home', HomePage)
])
