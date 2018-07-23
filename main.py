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
        user = users.get_current_user()
        variables = {}
        if user:
            nickname = user.nickname()
            logout_url = users.create_logout_url('/')
            variables ["log_url"] = logout_url
        else:
            login_url = users.create_login_url('/')
            variables ["log_url"] = login_url

        info = jinja_env.get_template('templates/info.html')
        self.response.write(info.render(variables))

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
