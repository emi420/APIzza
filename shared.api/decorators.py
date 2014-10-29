import json
import requests
from django.http import HttpResponse
import re

KEYS_API_URL = "http://localhost:7999/"

''' Headers access-control '''

def set_access_control_headers(response):
    response['Access-Control-Max-Age'] = 1000
    response['Access-Control-Allow-Headers'] = 'origin, x-csrftoken, content-type, accept, x-voolks-api-key, x-voolks-app-id, x-voolks-session-id'

class HttpOptionsDecorator(object):

    def __init__(self, f):
        self.f = f;

    def __call__(self, *args):
        response = self.f(*args)
        set_access_control_headers(response)
        return response
        

''' Decorator '''

class VoolksAPIAuthRequired(object):

    def __init__(self, f):
        self.f = f;

    def __call__(self, *args):

        request = args[0]

        key = request.META.get('HTTP_X_VOOLKS_API_KEY')
        app = request.META.get('HTTP_X_VOOLKS_APP_ID')

        if not key:
            try:
                key = request.GET.get('VoolksApiKey')
                app = request.GET.get('VoolksAppId')
            except(e):
                pass

        # Call external API (key.api)
        r = requests.get(KEYS_API_URL + 'check_key/', headers={'X-Voolks-App-Id': app, 'X-Voolks-Api-Key': key},verify=False)

        if not app or not key or r.status_code != 200:
        # If error. return response
            res = {}
            res['code'] = r.status_code
            res['text'] = "API authtentication failed"
            response = HttpResponse(json.dumps(res), content_type="application/json")
            response['Access-Control-Allow-Origin'] = '*'
            return response
        else:
            
            responseObj =  json.loads(r.text)

            # Check domain matching referer
            referer = request.META.get('HTTP_REFERER')
            if not referer:
                referer = ''
            # remove the protocol and split the url at the slashes
            referer = re.sub('^https?:\/\/', '', referer).split('/')
            if referer[0] != responseObj['domain'] and responseObj['domain'] != '*':
                res = {}
                res['code'] = 400
                res['text'] = "API permission denied - Invalid domain"
                response = HttpResponse(json.dumps(res), content_type="application/json")
                response['Access-Control-Allow-Origin'] = '*'
                return response
            
            # Check for general (delete, get, put, create) permissions
            elif (
                (request.META["REQUEST_METHOD"] == "DELETE" and responseObj['permissions'].find("-delete") >= 0) or
                (request.META["REQUEST_METHOD"] == "GET" and responseObj['permissions'].find("-get") >= 0) or
                (request.META["REQUEST_METHOD"] == "PUT" and responseObj['permissions'].find("-put") >= 0) or
                (request.META["REQUEST_METHOD"] == "POST" and responseObj['permissions'].find("-create") >= 0)
               ):
                res = {}
                res['code'] = 400
                res['text'] = "API permission denied"
                
                response = HttpResponse(json.dumps(res), content_type="application/json")
                response['Access-Control-Allow-Origin'] = '*'
                return response

            # Check for general "where" clause/parameter permissions
            elif request.META["REQUEST_METHOD"] == "GET" and responseObj['permissions'].find("-where") >= 0 and "where" in request.GET:
                res = {}
                res['code'] = 400
                res['text'] = "API permission denied"
                response = HttpResponse(json.dumps(res), content_type="application/json")
                response['Access-Control-Allow-Origin'] = '*'
                return response

            # Check for class data.api class creation permission
            elif request.get_full_path().find("/classes/") >= 0 and (request.META["REQUEST_METHOD"] == "PUT" or request.META["REQUEST_METHOD"] == "POST") and responseObj['permissions'].find("-classCreation") >= 0:

                # Get last record added in this class
                tmp_last_req = requests.get("http://" + request.get_host() + "/classes/" + (request.get_full_path().split('/'))[2] + """?sort={"_id":-1}&limit=1""", headers={'X-Voolks-App-Id': app, 'X-Voolks-Api-Key': key},verify=False)

                # If request for last record added was ok
                if tmp_last_req.status_code == 200:

                    # Last record added to class
                    tmp_last =  json.loads(tmp_last_req.text)

                    # Check if request ask for creation of new class
                    if not tmp_last: # is empty?
                        res = {}
                        res['code'] = 400
                        res['text'] = "API permission denied"
                        response = HttpResponse(json.dumps(res), content_type="application/json")
                        response['Access-Control-Allow-Origin'] = '*'
                        return response

                    # Check if request ask for insert or update of existing class, but with different structure
                    tmp_data_req = {}
                    if request.META["REQUEST_METHOD"] == "PUT":
                        tmp_data_req = request.PUT.items()[0][0]
                    else: # POST
                        tmp_data_req = request.POST.items()[0][0]
                    tmp_data = json.loads(tmp_data_req)
                    new_fields_requested = False
                    for key in tmp_data:
                        if not key in tmp_last['result'][0]:
                            new_fields_requested = True
                            break
                    if new_fields_requested:
                        res = {}
                        res['code'] = 400
                        res['text'] = "API permission denied"
                        response = HttpResponse(json.dumps(res), content_type="application/json")
                        response['Access-Control-Allow-Origin'] = '*'
                        return response

                else:
                    # Internal error getting last added record
                    res = {}
                    res['code'] = 400
                    res['text'] = "API permission denied * INTERNAL ERROR"
                    response = HttpResponse(json.dumps(res), content_type="application/json")
                    response['Access-Control-Allow-Origin'] = '*'
                    return response

            response = self.f(*args)
            response['Access-Control-Allow-Origin'] = responseObj['domain']
            
            # xxx
            # response['Access-Control-Allow-Methods'] = responseObj['permissions']
            
            # FIXME CHECK
            response['Access-Control-Allow-Methods'] = "GET,DELETE,POST,OPTIONS,PUT"
            
            return response
            
            

