import json
from decorators import HttpOptionsDecorator, VoolksAPIAuthRequired
from django.http import HttpResponse
from pymongo import Connection
from bson.objectid import ObjectId
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

USER_SESSION_URL = "http://localhost:8000/users/"
#USER_SESSION_URL = "http://auth.voolks.com/users/"
DATABASE_NAME = "test"

def get_api_credentials(request):
    ''' Get app id and api key '''

    app = request.META.get('HTTP_X_VOOLKS_APP_ID')
    if not app:
        app = request.GET.get('VoolksAppId','')
    key = request.META.get('HTTP_X_VOOLKS_API_KEY')
    if not key:
        key = request.GET.get('VoolksApiKey','')
    
    return (app, key)
    

@csrf_exempt
@HttpOptionsDecorator
@VoolksAPIAuthRequired
def classes(request, class_name):
    ''' Get, Delete, Count or Update multiple items'''
    ''' Create a single item '''

    response = {}
    sessionid = request.GET.get("sessionid", "")
    delete = False
    (app, key) = get_api_credentials(request)
    connection = Connection()
    db = connection[DATABASE_NAME]    
    instance = db[app + "-" + class_name]
    cur = None
    count = 0
    result = []
    request_delete = request.META["REQUEST_METHOD"] == "DELETE"
    request_post = request.META["REQUEST_METHOD"] == "POST"
    
    if request_post:
        
        # Create 
        
        data = request.POST.items()[0][0]
        parsed_data = json.loads(data)
        parsed_data['createdAt'] = str(datetime.now())
        obj = instance.insert(parsed_data)
        response['id'] = str(obj)
        
    else:

        # Get data

        if "where" in request.GET:
            query = json.loads(request.GET["where"])
        else:
            query = {}

        # Make query for permissions
        
        if not sessionid:
            if request_delete:

                query["$or"] = [
                    {"_mod":{"$exists": False}},
                    {"_mod":{"*":"*"}}, 
                    {"_mod":{"*":"write"}}
                ]
        
            else:

                query["$or"] = [
                    {"_mod":{"$exists": False}},
                    {"_mod":{"*":"*"}}, 
                    {"_mod":{"*":"read"}}
                ]
        else:

            session = validate_session(sessionid, app, key)

            if "userid" in session:
                userid = str(session['userid'])

            if request_delete:

                query["$or"] = [
                    {"_mod":{"$exists": False}},
                    {"_mod":{"*":"*"}}, 
                    {"_mod":{"*":"write"}}, 
                    {"_mod":{userid:"*"}}, 
                    {"_mod":{userid:"write"}}
                ]
                
            else:

                query["$or"] = [
                    {"_mod":{"$exists": False}},
                    {"_mod":{"*":"*"}}, 
                    {"_mod":{"*":"read"}}, 
                    {"_mod":{userid:"read"}}
                ]
                
                                
        # Get
        
        if not request_delete:
            cur = instance.find(query)

        # Delete

        else:
            instance.remove(query)
                
        # Count
        
        if cur:
            count = cur.count()
            if "count" in request.GET and request.GET["count"] == "true":
                result = {}
                result["count"] = count
            else:

                if not request_delete:

                    # Response

                    for i in range(0, count):
                        obj = cur.next()
                        obj['id'] = str(obj['_id'])
                        del obj['_id']
                        result.append(obj)

    if len(result) > 0:
        response['result'] = result
    
    return HttpResponse(json.dumps(response) + "\n", content_type="application/json")


def validate_session(sessionid, app, key):
    ''' Check if user session is valid using an external API (auth.api)'''

    import requests
    res = requests.get(USER_SESSION_URL + 'validate_session/?sessionid=' + sessionid, headers={'X-Voolks-App-Id': app, 'X-Voolks-Api-Key': key},verify=False)    
    return json.loads(res.text)



@csrf_exempt
@HttpOptionsDecorator
@VoolksAPIAuthRequired
def classes_get_one(request, class_name, obj_id):
    ''' Get, Delete or Update one item'''

    response = {}
    parsed_data = {}
    sessionid = request.GET.get("sessionid", "")
    (app, key) = get_api_credentials(request)
    connection = Connection()
    db = connection[DATABASE_NAME]
    instance = db[app + "-" + class_name]
    obj = None
    userid = None
    request_delete = request.META["REQUEST_METHOD"] == "DELETE"
    request_put = request.META["REQUEST_METHOD"] == "PUT"
    

    if obj_id and obj_id is not "":

        query = {}
        query["_id"] = ObjectId(obj_id)

        # Make query for permissions
        
        if not sessionid:

            if request_delete or request_put:

                query["$or"] = [
                    {"_mod":{"$exists": False}},
                    {"_mod":{"*":"*"}}, 
                    {"_mod":{"*":"write"}}
                ]
            
            else:

                query["$or"] = [
                    {"_mod":{"$exists": False}},
                    {"_mod":{"*":"*"}}, 
                    {"_mod":{"*":"read"}}
                ]

        else:

            session = validate_session(sessionid, app, key)

            if "userid" in session:
                userid = str(session['userid'])


            if request_delete or request_put:

                query["$or"] = [
                    {"_mod":{"$exists": False}},
                    {"_mod":{"*":"*"}}, 
                    {"_mod":{"*":"write"}}, 
                    {"_mod":{userid:"*"}}, 
                    {"_mod":{userid:"write"}}
                ]
                
            else:

                query["$or"] = [
                    {"_mod":{"$exists": False}},
                    {"_mod":{"*":"*"}}, 
                    {"_mod":{"*":"read"}}, 
                    {"_mod":{userid:"read"}}
                ]

        # Delete

        if request_delete:
            instance.remove(query, True)
        
        # Get 

        else:
            obj = instance.find_one(query)

        if obj:
            obj['id'] = obj_id

            # Update

            if request_put:
                data = request.read()
                parsed_data = json.loads(data)
                parsed_data['updatedAt'] = str(datetime.now())
                instance.update(query, parsed_data)
                obj = instance.find_one(query)


            # Response
            
            del obj["_id"]
            parsed_data = obj

        else:
            parsed_data = {}
                
        return HttpResponse(json.dumps(parsed_data) + "\n", content_type="application/json")
        
    else:
        return HttpResponse(json.dumps({}), content_type="application/json")
        
    
    
