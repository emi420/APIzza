import json
import requests
from django.http import HttpResponse
from django.contrib.auth import authenticate

#KEYS_API_URL = "http://key.voolks.com/"
KEYS_API_URL = "http://localhost:7999/"


''' Headers access-control '''

def set_access_control_headers(response):

    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'PUT, DELETE, POST, GET, OPTIONS'
    response['Access-Control-Max-Age'] = 1000
    response['Access-Control-Allow-Headers'] = 'origin, x-csrftoken, content-type, accept'

class HttpOptionsDecorator(object):

    def __init__(self, f):
        self.f = f;

    def __call__(self, *args):
        request = args[0]
        response = self.f(*args)
        set_access_control_headers(response)
        return response
        

''' Decorator '''

def VoolksAPIAuthRequired(function):

  def wrap(request, *args, **kwargs):

        key = request.META.get('HTTP_X_VOOLKS_API_KEY')
        app = request.META.get('HTTP_X_VOOLKS_APP_ID')
        if not key or not app:
            key = request.GET.get('VoolksApiKey','')
            app = request.GET.get('VoolksAppId','')
            
        # Call external API (key.api)
        r = requests.get(KEYS_API_URL + 'check_key/', headers={'X-Voolks-App-Id': app, 'X-Voolks-Api-Key': key},verify=False)

        if not app or not key or r.status_code != 200:
        # If error. return response
            response = {}
            response['code'] = 666
            response['text'] = "Voolks API authtentication failed"
            return HttpResponse(json.dumps(response), content_type="application/json")
        else:
            # If auth ok, continue
            return function(request, *args, **kwargs)

  wrap.__doc__=function.__doc__
  wrap.__name__=function.__name__
  return wrap
