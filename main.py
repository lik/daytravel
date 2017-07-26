from __future__ import print_function

import argparse
import json
import pprint
import requests
import sys
import urllib
import logging

from urllib2 import HTTPError
from urllib import quote
from urllib import urlencode

import webapp2
import os
import jinja2

from google.appengine.api import urlfetch
from google.appengine.api import users
from google.appengine.ext import ndb

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

# OAuth credential placeholders that must be filled in by users.
# You can find them on https://www.yelp.com/developers/v3/manage_app
# ???? Do these need to be new credentials every time? Will this ID and Secret
# expire at some point??
CLIENT_ID = 'lVS7Jp-d_F0d1MAr-G6pVA'
CLIENT_SECRET = '1oeh0AXp46hM6SeTNOWD2DuerIzg7GiHAkgRsibL7wPiv8zUcC7z3nD6NNZhsL1G'


# API constants, you shouldn't have to change these.
API_HOST = 'http://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.
TOKEN_PATH = '/oauth2/token'
GRANT_TYPE = 'client_credentials'


# Defaults for our simple example.
DEFAULT_TERM = 'dinner'
DEFAULT_LOCATION = 'San Francisco, CA'
SEARCH_LIMIT = 3


def obtain_bearer_token(host, path):
    """Given a bearer token, send a GET request to the API.

    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        params (dict): An optional set of query parameters in the request.

    Returns:
        str: OAuth bearer token, obtained using client_id and client_secret.

    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    data = urlencode({
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': GRANT_TYPE,
    })
    print('@@@@@@@@@' + CLIENT_ID)
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
    }
    result = urlfetch.fetch(
        url=url,
        payload=data,
        method=urlfetch.POST,
        headers=headers)
    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@' + result.content)
    return "BIO6_LpbIcFkeKDB9SsSAONt3lE2IwrdiTxUeq-Ag1MKOzSc4m-8QyPjdV6WmI27ySuLEKv7czHoJmJjFHrCyjfgxucTvKPpJG9JCsg_08KCz4J-WrEfeaiACoJ2WXYx"


def request(host, path, bearer_token, params):
    """Given a bearer token, send a GET request to the API.

    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        bearer_token (str): OAuth bearer token, obtained using client_id and client_secret.
        params (dict): An optional set of query parameters in the request.

    Returns:
        dict: The JSON response from the request.

    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url = '{0}{1}?{2}'.format(
      host,
      quote(path.encode('utf8')),
      urllib.urlencode(params))
    headers = {
        'Authorization': 'Bearer %s' % bearer_token,
    }

    logging.info(u'Querying {0} ...'.format(url))
    result = urlfetch.fetch(
        url=url,
        method=urlfetch.GET,
        headers=headers)
    logging.info('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@' + result.content)
    return json.loads(result.content)


def search(bearer_token, term, location):
    """Query the Search API by a search term and location.

    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.

    Returns:
        dict: The JSON response from the request.
    """

    params = {
        'term': term,
        'location': location,
        'limit': SEARCH_LIMIT
    }
    return request(API_HOST, SEARCH_PATH, bearer_token, params=params)


def get_business(bearer_token, business_id):
    """Query the Business API by a business ID.

    Args:
        business_id (str): The ID of the business to query.

    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id
    return request(API_HOST, business_path, bearer_token)


# important
def query_api(term, location):
    """Queries the API by the input values from the user.

    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    bearer_token = obtain_bearer_token(API_HOST, TOKEN_PATH)

    response = search(bearer_token, term, location)

'''
    businesses = response.get('businesses')

    if not businesses:
        print(u'No businesses for {0} in {1} found.'.format(term, location))
        return

    business_id = businesses[0]['id']

    print(u'{0} businesses found, querying business info ' \
        'for the top result "{1}" ...'.format(
            len(businesses), business_id))
    response = get_business(bearer_token, business_id)

    print(u'Result for business "{0}" found:'.format(business_id))
    pprint.pprint(response, indent=2)
'''


class Profile(ndb.Model):
    name = ndb.StringProperty()

profile = Profile(name="Adina Wallis")
key = profile.put()


class City(ndb.Model):
    name = ndb.StringProperty()


class ActivityType(ndb.Model):
    name = ndb.StringProperty()


class Results(ndb.Model):
    activitytype_key = ndb.KeyProperty(kind=ActivityType)
    suggestion = ndb.StringProperty()
    city_key = ndb.KeyProperty(kind=City)
    profile_key = ndb.KeyProperty(kind=Profile)


class DayPlan(ndb.Model):
    user = ndb.StringProperty()
    # repeated property makes 'results' into a list
    results = ndb.KeyProperty(kind=Results, repeated=True)
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
        city= self.request.get('city')
        current_user = users.get_current_user()
        logout_url= users.create_logout_url('/')
        login_url= users.create_login_url('/')

        self.redirect('/plan?city=' + city)


class PlanHandler(webapp2.RequestHandler):
    def get(self):
        city = self.request.get('city')
        logout_url = users.create_logout_url('/')

        template = jinja_environment.get_template("templates/plan.html")
        template_vars = {
            'city': city,
            'logout_url': logout_url,
        }
        self.response.write(template.render(template_vars))
    def post(self):
        city = self.request.get('city')
        activities = self.request.get_all('activity')
        logout_url = users.create_logout_url('/')
        bearer_token = obtain_bearer_token(API_HOST, TOKEN_PATH)
        #this is where we pass in form input
        response = search(bearer_token, activities[0], city)
        self.redirect('/results?city=' + city + '&activity=' + ','.join(activities))


class ResultsHandler(webapp2.RequestHandler):
    def get(self):
        city= self.request.get('city')
        activities = self.request.get_all('activity')
        logout_url = users.create_logout_url('/')
        activities_str = ','.join(activities)
        activities_dict = dict((k.strip(), v.strip()) for k,v in
              (item.split('.') for item in activities_str.split(',')))
        print(activities_dict)

        template = jinja_environment.get_template("templates/results.html")
        template_vars = {
            'city': city,
            'activities': activities,
            'logout_url': logout_url,
        }
        self.response.write(template.render(template_vars))
    def post(self):
        city= self.request.get('city')
        activity = self.request.get_all('activity')
        logout_url = users.create_logout_url('/')


class BrowseHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("templates/browse.html")
        self.response.write(template.render())


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/plan', PlanHandler),
    ('/browse', BrowseHandler),
    ('/results', ResultsHandler),

], debug=True)
