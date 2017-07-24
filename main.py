import webapp2
import os
import jinja2

from google.appengine.api import users
from google.appengine.ext import ndb

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class Activity(ndb.Model):
    name = ndb.StringProperty()

class Result(ndb.Model):
    activity_key = ndb.KeyProperty(kind=Activity)
    suggestion = ndb.StringProperty()

class DayPlan(ndb.Model):
    user = ndb.StringProperty()
    results = ndb.KeyProperty(kind=Result, repeated=True)
    city = ndb.StringProperty()

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("templates/daytravel.html")
        self.response.write(template.render())




class PlanHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(template.render())





class BrowseHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(template.render())




class ResultsHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(template.render())







app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/planhandler', PlanHandler),
    ('/browsehandler', BrowseHandler),
    ('/resultshandler', ResultsHandler),

], debug=True)
