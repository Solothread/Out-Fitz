import jinja2
import webapp2
import os
import json
import urllib
import urllib2
import datetime
from google.appengine.ext import ndb
from google.appengine.api import users
from models import Visitor

jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)))

class Login(ndb.Model):
    login_url = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    nickname = ndb.StringProperty(required=True)
class Outfit(ndb.Model):
    outfitdef = ndb.StringProperty(required=False)
    datepick = ndb.StringProperty()

class Entry(ndb.Model):
    date = ndb.StringProperty(required=True)
    label = ndb.StringProperty(required=True)
    link = ndb.StringProperty(required=True)

class InfoPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user: #User is not signed in
            info = jinja_env.get_template('templates/info.html')
            jinja_values = {
                'log_url': users.create_login_url('/')
            }
            self.response.write(info.render(jinja_values))
        else: #User is signed in
            my_key = ndb.Key('Visitor', user.user_id())
            my_visitor = my_key.get()
            #Check data store, do we already have the users data?
            # if not: Create new entry in datastore for user
            if not my_visitor:
                my_visitor = Visitor(
                    key = my_key,
                    id = user.user_id(),
                    name = user.nickname(),
                    email = user.email())
                my_visitor.put()

            userhome = jinja_env.get_template('templates/home.html')
            jinja_values = {
                'name': user.nickname(),
                'email_addr': user.email(),
                'user_id': user.user_id(),
                'log_url': users.create_logout_url('/'),
                'month': datetime.datetime.now().strftime("%A, %B %d, %Y")
            }
            self.response.write(userhome.render(jinja_values))

    def post(self):
        outfit_description = self.request.get("outfitdescription")
        date_picker = self.request.get("datepicker")

        my_outfit = Outfit(
            outfitdef = outfit_description,
            datepick = date_picker)
        my_outfit.put()

        jinja_value = {
        "outfitdescription": outfit_description,
        "datepicker": date_picker,
                                    }

        entriesTemplate = jinja_env.get_template("/templates/home.html")
        self.response.write(entriesTemplate.render(jinja_value))


app = webapp2.WSGIApplication([
    ('/', InfoPage),
])
