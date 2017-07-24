import webapp2
import os
import jinja2

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("templates/daytravel.html")
        self.response.write(template.render())

class PlanHandler(webapps2.RequestHandler):
    def get(self):
        self.response.write(template.render())

class BrowseHandler(webapps2.RequestHandler):
    def get(self):
        self.response.write(template.render())

class ResultsHandler(webapps2.RequestHandler):
    def get(self):
        self.response.write(template.render())





app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/planhandler', PlanHandler),
    ('/browsehandler', BrowseHandler),
    ('/resultshandler', ResultsHandler),

], debug=True)
