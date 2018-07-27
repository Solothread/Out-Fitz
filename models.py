from google.appengine.ext import ndb

class Visitor(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    id = ndb.StringProperty()
    image = ndb.BlobProperty()

class Outfit(ndb.Model):
    Description = ndb.StringProperty(required=False)
    Date = ndb.StringProperty(required=False)
    Image = ndb.TextProperty()
    User_ID = ndb.StringProperty()
    deleteButton = ndb.BooleanProperty(required=False)
