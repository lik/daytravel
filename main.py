import webapp2
import os
import jinja2

from google.appengine.api import users
from google.appengine.ext import ndb

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class Username(ndb.Model):
    user = ndb.StringProperty()

class City(ndb.Model):
    city = ndb.StringProperty()

class Activity(ndb.Model):
    name = ndb.StringProperty()

class Result(ndb.Model):
    activity_key = ndb.KeyProperty(kind=Activity)
    suggestion = ndb.StringProperty()

class DayPlan(ndb.Model):
    user = ndb.StringProperty()
    # repeated property makes 'results' into a list
    results = ndb.KeyProperty(kind=Result, repeated=True)
    city = ndb.StringProperty()



class MainHandler(webapp2.RequestHandler):
    def get(self):
        current_user = users.get_current_user()
        logout_url= users.create_logout_url('/')
        login_url= users.create_login_url('/')

        template = jinja_environment.get_template("templates/daytravel.html")
        template_vars = {
        'current_user': current_user,
        'logout_url': logout_url,
        'login_url': login_url,
        }
        self.response.write(template.render(template_vars))

    def post(self):
        current_user = users.get_current_user()
        logout_url= users.create_logout_url('/')
        login_url= users.create_login_url('/')

        self.redirect('/plan')




class PlanHandler(webapp2.RequestHandler):
    def get(self):
        City_Query =City.query()
        city = City_Query.fetch()

        template = jinja_environment.get_template("templates/plan.html")
        template_vars = {
        'city': city,
        }
        self.response.write(template.render(template_vars))
    def post(self):
        activity = self.request.get('subActivity')





class BrowseHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("templates/browse.html")
        self.response.write(template.render())




class ResultsHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("templates/results.html")
        self.response.write(template.render())



app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/plan', PlanHandler),
    ('/browse', BrowseHandler),
    ('/results', ResultsHandler),

], debug=True)
