import requests
from decorators import HttpOptionsDecorator, VoolksAPIAuthRequired
from django.http import HttpResponse, HttpResponseRedirect
from pymongo import Connection
import json
from datetime import datetime
import urllib
import re

DATABASE_NAME = "testgeo"
INSTANCE_NAME = "testgeo1"

@HttpOptionsDecorator
@VoolksAPIAuthRequired
def savegeo(request):
    response = {}
    connection = Connection()
    db = connection[DATABASE_NAME]    
    instance = db[INSTANCE_NAME]
    try:
        instance.ensureIndex([("myPosition", pymongo.GEOSPHERE)])
    except:
        # XXX
        x = 1

    request_post = request.META["REQUEST_METHOD"] == "POST"
    try:
        request_content_type_json = request.META["CONTENT_TYPE"] == "application/json; charset=UTF-8"
    except:
        request_content_type_json = False

    if request_post:
        data = []
        # Create 
        if request_content_type_json:
            decode = urllib.unquote(request.body)
            decode = decode.replace("[","|")
            decode = decode.replace("]","|")
            decode = decode.replace("=","")
            decode = decode.replace("|||","|")
            sp = decode.split('&')
            sp0 = sp[0].split("|")
            sp1 = sp[1].split("|")
            sp2 = sp[2].split("|")
                        
            data = '{'
            data = data + '"' + sp0[0] + '":{' 
            data = data + '"' + sp0[1] + '":' + '"' + sp0[2] + '",'
            data = data + '"' + sp1[1] + '":' + '[' + sp1[2] + ',' + sp2[2] + ']'
            data = data + '}'
            data = data + '}'
            
        else:
            try:
                data = request.body
            except:
                data = request.POST.items()[0][0]
            
        parsed_data = json.loads(data)
        '''try:
            parsed_data = json.loads(data)
        except:
            return HttpResponse(json.dumps({"error":"Invalid JSON","code":"533"}) + "\n", content_type="application/json")
        '''
        parsed_data['createdAt'] = str(datetime.now())
        obj = instance.insert(parsed_data)
        response['id'] = str(obj)
            
    return HttpResponse(json.dumps(response) + "\n", content_type="application/json")
        