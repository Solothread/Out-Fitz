from google.appengine.ext import ndb

class Visitor(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    id = ndb.StringProperty()
    image = ndb.BlobProperty()

class Outfit(ndb.Model):
    Description = ndb.StringProperty(required=False)
    Date = ndb.StringProperty()
    Image = ndb.StringProperty(required=False)
    User_ID = ndb.StringProperty()
