from google.appengine.ext import ndb

class Visitor(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    id = ndb.StringProperty()
    image = ndb.BlobProperty()

class Outfit(ndb.Model):
    outfitdef = ndb.StringProperty(required=False)
    datepick = ndb.StringProperty()
    link = ndb.StringProperty(required=True)
