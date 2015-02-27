import requests
import pymongo
from pymongo import Connection
from decorators import HttpOptionsDecorator, VoolksAPIAuthRequired
from django.http import HttpResponse, HttpResponseRedirect
import json
from bson.objectid import ObjectId
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import urllib
import re
from gcm import * 

DATABASE_NAME = "testpushdb"
INSTANCE_NAME = "testpushin"
API_KEY = "AIzaSyBZCucRM2dC7D9f71S9HzNHgoY409uvxHU"

def get_api_credentials(request):
    ''' Get app id and api key '''

    app = request.META.get('HTTP_X_VOOLKS_APP_ID')
    key = request.META.get('HTTP_X_VOOLKS_API_KEY')
    
    return (app, key)

@HttpOptionsDecorator
@VoolksAPIAuthRequired
def installations(request):
    ''' Create installation log device '''

    response = {}
    parsed_data = {}
    (app, key) = get_api_credentials(request)
    connection = Connection()
    db = connection[DATABASE_NAME]
    instance = db[INSTANCE_NAME]

    request_post = request.META["REQUEST_METHOD"] == "POST"
    request_content_type_json = request.META.get('CONTENT_TYPE') == "application/json; charset=UTF-8"

    if request_post:
    
        # Create 
        if request_content_type_json:
            data = "{"
            params = dict([p.split('=') for p in request.body.split('&')])
            for key2 in params: 
                data = data + '"' + key2 + '":"' +params[key2] + '",'
            data = data + "}"
            data = data.replace(",}","}")
        else:
            try:
                data = request.body
            except:
                data = request.POST.items()[0][0]
            
        parsed_data = json.loads(data)

        try:
            parsed_data['createdAt'] = str(datetime.now())
            obj = db.instance.insert(parsed_data)
            response['id'] = str(obj)
            return HttpResponse(json.dumps(response) + "\n", content_type="application/json")
        except:
            # Can't create log device
            response['code'] = 52
            response['text'] = "Can't create installation log device"
            return HttpResponse(json.dumps(response) + "\n", content_type="application/json")

@csrf_exempt
@HttpOptionsDecorator
@VoolksAPIAuthRequired
def delete(request): 
    ''' Delete one installation'''

    response = {}
    (app, key) = get_api_credentials(request)
    connection = Connection()
    db = connection[DATABASE_NAME]
    instance = db[INSTANCE_NAME]
    
    objid = request.GET.get('objid','')
    
    try:
        db.instance.remove({'_id': ObjectId(objid)})
    except:
        # Can't delete log device
    
        response['code'] = 57
        response['text'] = "Can't delete log device"
        return HttpResponse(json.dumps(response) + "\n", content_type="application/json")

    # Build response
    
    response['code'] = 1
    response['text'] = "Log device deleted"
    return HttpResponse(json.dumps(response) + "\n", content_type="application/json")    

        
@csrf_exempt
@HttpOptionsDecorator
@VoolksAPIAuthRequired
def push(request):         
    ''' Send push notification to installations'''
    
    response = {}
    parsed_data = {}
    (app, key) = get_api_credentials(request)
    connection = Connection()
    db = connection[DATABASE_NAME]
    instance = db[INSTANCE_NAME]
    cur = None
    count = 0
    result = []
    
    request_post = request.META["REQUEST_METHOD"] == "POST"
    request_content_type_json = request.META.get('CONTENT_TYPE') == "application/json; charset=UTF-8"
    
    if request_post:
        if request_content_type_json:
            data = request.body
            data = "{"
            params = dict([p.split('=') for p in request.body.split('&')])
            for key2 in params: 
                data = data + '"' + key2 + '":"' +params[key2] + '",'
            data = data + "}"
            data = data.replace(",}","}")
        else:
            try:
                data = request.body
            except:
                data = request.POST.items()[0][0]
            
        parsed_data = json.loads(data)
        
        # Get data
        
        if "where" in parsed_data:
            query = parsed_data["where"]
            if type(query) is dict:
                cur = db.instance.find(query)
                
        if cur:
            # Response
            
            for i in cur:
                obj = cur.next()
                obj['id'] = str(obj['_id'])
                del obj['_id']
                result.append(obj)
                
                # Android
                if obj['deviceType'] == 'android':
                    
                    reg_id = str(obj['deviceToken'])
                    data = parsed_data['data']
                    
                    gcm = GCM(API_KEY)
                    gcm.plaintext_request(registration_id=reg_id, data=data)
                        
        return HttpResponse(json.dumps(response) + "\n", content_type="application/json")
                
@csrf_exempt
@HttpOptionsDecorator
@VoolksAPIAuthRequired
def push_one(request, obj_id):         
    ''' Send push notification to an installation'''
    
    response = {}
    parsed_data = {}
    (app, key) = get_api_credentials(request)
    connection = Connection()
    db = connection[DATABASE_NAME]
    instance = db[INSTANCE_NAME]
    
    request_post = request.META["REQUEST_METHOD"] == "POST"
    request_content_type_json = request.META.get('CONTENT_TYPE') == "application/json; charset=UTF-8"
    
    if request_post:
        if request_content_type_json:
            data = request.body
            data = "{"
            params = dict([p.split('=') for p in request.body.split('&')])
            for key2 in params: 
                data = data + '"' + key2 + '":"' +params[key2] + '",'
            data = data + "}"
            data = data.replace(",}","}")
        else:
            try:
                data = request.body
            except:
                data = request.POST.items()[0][0]
            
        parsed_data = json.loads(data)
        
        if obj_id and obj_id is not "":
        
            # Get data
            
            obj = db.instance.find_one({'_id': ObjectId(obj_id)})
                        
            # Android
            if obj['deviceType'] == 'android':
                
                reg_id = str(obj['deviceToken'])
                data = parsed_data['data']
                                
                gcm = GCM(API_KEY)
                gcm.plaintext_request(registration_id=reg_id, data=data)
                
        return HttpResponse(json.dumps(response) + "\n", content_type="application/json")
    

    
