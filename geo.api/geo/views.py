import requests
import pymongo
from decorators import HttpOptionsDecorator, VoolksAPIAuthRequired
from django.http import HttpResponse, HttpResponseRedirect
from pymongo import Connection, GEOSPHERE, GEO2D
import json
from datetime import datetime
import urllib
import re

# DATABASE_NAME = "testgeo"
# INSTANCE_NAME = "point"

@HttpOptionsDecorator
@VoolksAPIAuthRequired
def savegeo(request):
    response = {}
    db = Connection().testgeo
    # XXX
    # eval("db = Connection()."+DATABASE_NAME)  
    try:
        db.point.ensure_index([("myPosition", GEOSPHERE)]) 
    except Exception as e:
        return HttpResponse(json.dumps({"error":"Ensuring GEOSPHERE: " + type(e).__name__ + ": " + e.message, "code":"534"}) + "\n", content_type="application/json")

    request_post = request.META["REQUEST_METHOD"] == "POST"
    request_content_type_json = request.META.get('CONTENT_TYPE') == "application/json; charset=UTF-8"

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
        obj = db.point.insert(parsed_data)
        response['id'] = str(obj)
            
    return HttpResponse(json.dumps(response) + "\n", content_type="application/json")

@HttpOptionsDecorator
@VoolksAPIAuthRequired
def neargeo(request):
    response = {}
    db = Connection().testgeo
    cur = None
    count = 0
    result = []
    try:
        db.point.ensure_index([("myPosition", GEOSPHERE)])
    except Exception as e:
        return HttpResponse(json.dumps({"error":"Ensuring GEOSPHERE: " + type(e).__name__ + ": " + e.message, "code":"534"}) + "\n", content_type="application/json")
        
    # Get data

    if "where" in request.GET:

        query = json.loads(request.GET["where"])
        cur = db.point.find(query)

    # Count     

    if cur:
        count = cur.count()
        
        # Response

        for i in range(0, count):
            obj = cur.next()
            obj['id'] = str(obj['_id'])
            del obj['_id']
            result.append(obj)

    if len(result) > 0:
        response['result'] = result
        
    return HttpResponse(json.dumps(response) + "\n", content_type="application/json")        

@HttpOptionsDecorator
@VoolksAPIAuthRequired
def withingeo(request):
    response = {}
    connection = Connection()
    db = Connection().testgeo
    cur = None
    count = 0
    result = []
    try:
        db.point.ensure_index([("myPosition", GEOSPHERE)])
    except Exception as e:
        return HttpResponse(json.dumps({"error":"Ensuring GEOSPHERE: " + type(e).__name__ + ": " + e.message, "code":"534"}) + "\n", content_type="application/json")

    # Get data

    if "where" in request.GET:

        query = json.loads(request.GET["where"])
        cur = db.point.find(query)

    # Count     

    if cur:
        count = cur.count()
        
        # Response

        for i in range(0, count):
            obj = cur.next()
            obj['id'] = str(obj['_id'])
            del obj['_id']
            result.append(obj)

    if len(result) > 0:
        response['result'] = result
        
    return HttpResponse(json.dumps(response) + "\n", content_type="application/json")    