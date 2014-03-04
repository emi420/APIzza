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
    cur2 = None
    count = 0
    count2 = 0
    result = []
    
    if request.META["REQUEST_METHOD"] == "POST":
        
        # Create 
        
        data = request.POST.items()[0][0]
        parsed_data = json.loads(data)
        parsed_data['createdAt'] = str(datetime.now())
        obj = instance.insert(parsed_data)
        response['id'] = str(obj)
        
    else:
        
        # Delete
        
        if request.META["REQUEST_METHOD"] == "DELETE":
            delete = True

        # Get data

        if "where" in request.GET:
            where = json.loads(request.GET["where"])
        else:
            where = {}

        where["_mod"] = {"$exists": False}
        if not delete:
            cur = instance.find(where)
        else:
            instance.remove(where)

        if sessionid:
            session = validate_session(sessionid, app, key)

            if "userid" in session:
                userid = str(session['userid'])
                where = {}
                where["_mod"] = {userid:"*"}
                if not delete:
                    cur2 = instance.find(where)
                else:
                    instance.remove(where)
                
        # Count
        
        if cur:
            count = cur.count()

        if cur2:
            count2 = cur2.count()

        # Response

        if delete is not True:

            for i in range(0, count):
                obj = cur.next()
                obj['id'] = str(obj['_id'])
                del obj['_id']
                result.append(obj)

            for i in range(0, count2):
                obj = cur2.next()
                obj['id'] = str(obj['_id'])
                del obj['_id']
                result.append(obj)
            
    if "count" in request.GET and request.GET["count"] == "true":
        result = {}
        result["count"] = count + count2

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
    delete = False
    sessionid = request.GET.get("sessionid", "")
    (app, key) = get_api_credentials(request)
    connection = Connection()
    db = connection[DATABASE_NAME]
    instance = db[app + "-" + class_name]
    obj = None

    if obj_id and obj_id is not "":

        # Get one item by id

        where = {}
        where["_id"] = ObjectId(obj_id)

        if not sessionid:
            where["_mod"] = {"$exists": False}

        else:

            session = validate_session(sessionid, app, key)

            if "userid" in session:
                userid = str(session['userid'])
                where["_mod"] = {userid:"*"}

        # Delete

        if request.META["REQUEST_METHOD"] == "DELETE":
            instance.remove(where, True)
        
        # Get 

        else:
            obj = instance.find_one(where)


        if obj:
            obj['id'] = obj_id

            # Update

            if request.META["REQUEST_METHOD"] == "PUT":
                data = request.read()
                parsed_data = json.loads(data)
                parsed_data['updatedAt'] = str(datetime.now())
                instance.update(where, parsed_data)
                obj = instance.find_one(where)


            del obj["_id"]
            parsed_data = obj

        else:
            parsed_data = {}
                
        return HttpResponse(json.dumps(parsed_data) + "\n", content_type="application/json")
        
    else:
        return HttpResponse(json.dumps({}), content_type="application/json")
        
    
    
