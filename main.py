from __future__ import print_function

import argparse
import json
import pprint
import requests
import sys
import urllib

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
        url_params (dict): An optional set of query parameters in the request.

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
    #bearer_token = json.decode(result.content)['access_token']
    #return bearer_token
    #response = requests.request('POST', url, data=data, headers=headers)
    #bearer_token = response.json()['access_token']
    #return bearer_token


def request(host, path, bearer_token, url_params=None):
    """Given a bearer token, send a GET request to the API.

    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        bearer_token (str): OAuth bearer token, obtained using client_id and client_secret.
        url_params (dict): An optional set of query parameters in the request.

    Returns:
        dict: The JSON response from the request.

    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % bearer_token,
    }

    print(u'Querying {0} ...'.format(url))

    result = urlfetch.fetch(
        url=url,
        params = urllib.urlencode({



        }),
        method=urlfetch.GET,
        headers=headers)
    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@' + result.content)
    return json.loads(result.content)
    #response = requests.request('GET', url, headers=headers, params=url_params)
    #return response.json()


def search(bearer_token, term, location):
    """Query the Search API by a search term and location.

    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.

    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT
    }
    return request(API_HOST, SEARCH_PATH, bearer_token, url_params=url_params)


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

def main_fusion():
    parser = argparse.ArgumentParser()

    parser.add_argument('-q', '--term', dest='term', default=DEFAULT_TERM,
                        type=str, help='Search term (default: %(default)s)')
    parser.add_argument('-l', '--location', dest='location',
                        default=DEFAULT_LOCATION, type=str,
                        help='Search location (default: %(default)s)')

    input_values = parser.parse_args()

    try:
        query_api(input_values.term, input_values.location)
    except HTTPError as error:
        sys.exit(
            'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                error.code,
                error.url,
                error.read(),
            )
        )






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

        self.redirect('/plan?city={{city}}')

class PlanHandler(webapp2.RequestHandler):
    def get(self):
        city= self.request.get('city')
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
        query_api('hiking', 'Mountain View, CA')








app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/plan', PlanHandler),
    ('/browse', BrowseHandler),
    ('/results', ResultsHandler),

], debug=True)
