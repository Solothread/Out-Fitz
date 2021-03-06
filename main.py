import jinja2
import webapp2
import os
import json
import urllib
import urllib2
import datetime
import base64
from google.appengine.ext import ndb
from google.appengine.api import users
from models import Visitor, Outfit

jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def get_key(me):
    return ndb.Key("Visitor", me.user_id())

def get_visitor():
    me = users.get_current_user()
    if not me:
        return None
    my_key = get_key(me)
    return my_key.get()

class DeleteHandler(webapp2.RequestHandler):
    def post(self):
        #delete outfit object
        print(self.request.get("data"))
        #outfit = Outfit.query(Outfit.id == self.request.get("data")).get()
        #print(outfit)
        ndb.Key("Outfit", int(self.request.get("data"))).delete()

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
            my_visitor = get_visitor()
            #Check data store, do we already have the users data?
            # if not: Create new entry in datastore for user
            if not my_visitor:
                my_visitor = Visitor(
                    #key = my_key,
                    id = user.user_id(),
                    name = user.nickname(),
                    email = user.email())

                my_visitor.put()

            userhome = jinja_env.get_template('templates/home.html')

            #Outfits query
            #Need to add filter
            query = Outfit.query(Outfit.User_ID == user.user_id()).order(-Outfit.Date)
            outfitslist = query.fetch()
            #Query end

            jinja_values = {
                'name': user.nickname(),
                'email_addr': user.email(),
                'user_id': user.user_id(),
                'log_url': users.create_logout_url('/'),
                'month': datetime.datetime.now().strftime("%A, %B %d, %Y"),
                'outfits': outfitslist
            }
            # if my_visitor.image:
            #     jinja_values["img"] = base64.b64encode(my_visitor.image)

            self.response.write(userhome.render(jinja_values))

    def post(self):
        user = users.get_current_user()
        my_visitor = get_visitor()

        # if my_visitor:
        img = self.request.get("myfile")
        visitorimage = base64.b64encode(img)
        # my_visitor.put()

        outfit_description = self.request.get("outfitdescription")
        date_picker = self.request.get("datepicker")
        pic_link = self.request.get("link")
        deleteButton = self.request.get("deleteButton")

        my_outfit = Outfit(
            Description = outfit_description,
            Date = date_picker,
            Image = visitorimage,
            User_ID = user.user_id())
        my_outfit.put()

        self.redirect('/')
        # query = Outfit.query()
        # outfitslist = query.fetch()
        # jinja_values = {
        #     'name': user.nickname(),
        #     'email_addr': user.email(),
        #     'user_id': user.user_id(),
        #     'log_url': users.create_logout_url('/'),
        #     'month': datetime.datetime.now().strftime("%A, %B %d, %Y"),
        #     "outfitdescription": outfit_description,
        #     "datepicker": date_picker,
        #     'outfits': outfitslist
        # }
        #
        # if visitorimage:
        #     jinja_values["img"] = base64.b64encode(visitorimage)
        #
        # entriesTemplate = jinja_env.get_template("/templates/home.html")
        # self.response.write(entriesTemplate.render(jinja_values))

app = webapp2.WSGIApplication([
    ('/', InfoPage),
    ('/delete', DeleteHandler),
])
