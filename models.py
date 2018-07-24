from google.appengine.ext import ndb

class Visitor(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    id = ndb.StringProperty()
