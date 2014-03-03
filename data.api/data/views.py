import json
from decorators import HttpOptionsDecorator, VoolksAPIAuthRequired
from django.http import HttpResponse
from pymongo import Connection
from bson.objectid import ObjectId
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

USER_SESSION_URL = "http://localhost:8000/users/"
#USER_SESSION_URL = "http://auth.voolks.com/users/"

@csrf_exempt
@HttpOptionsDecorator
@VoolksAPIAuthRequired
def classes(request, class_name):

    response = {}
    database_name = "test"
    connection = Connection()
    db = connection[database_name]
    
    sessionid = request.GET.get("sessionid", "")

    app = request.META.get('HTTP_X_VOOLKS_APP_ID')
    if not app:
        app = request.GET.get('VoolksAppId','')


    key = request.META.get('HTTP_X_VOOLKS_API_KEY')
    if not key:
        key = request.GET.get('VoolksApiKey','')
            
    instance = db[app + "-" + class_name]
    
    delete = False
    
    
    if request.META["REQUEST_METHOD"] == "POST":
        
        # Create 
        data = request.POST.items()[0][0]
        parsed_data = json.loads(data)
        parsed_data['createdAt'] = str(datetime.now())
        obj = instance.insert(parsed_data)
        response['id'] = str(obj)
        
    else:
        
        if "where" in request.GET:
            # Delete
            if request.META["REQUEST_METHOD"] == "DELETE":
                objs = json.loads(request.GET["where"])
                for o in objs:
                    if check_mod(o, "delete", sessionid, app, key):
                        instance.remove(o)
                delete = True
            
            # Count
            elif "count" in request.GET and request.GET["count"] == "True":
                cur = instance.find(json.loads(request.GET["where"]).count())
            
            else:
            # Where
                try:
                    cur = instance.find(json.loads(request.GET["where"]))
                except:
                    # FIXME CHECK
                    cur = instance.find(json.loads('{' + request.GET["where"] + '}'))
            
        else:
            # Delete
            if request.META["REQUEST_METHOD"] == "DELETE":
                objs = instance.find()
                for o in objs:
                    if check_mod(o, "delete", sessionid, app, key):
                        instance.remove(o)
                
                delete = True

            # Count
            elif "count" in request.GET and request.GET["count"] == "true":
                cur = instance.find().count()
            
            # Get all
            else:
                cur = instance.find()

        
        result = []
        
        # Count
        if "count" in request.GET and request.GET["count"] == "true":
            result = {}
            result["count"] = cur

        else:
            if delete is not True:
                for i in range(0, cur.count()):
                    obj = cur.next()
                    obj['id'] = str(obj['_id'])
                    del obj['_id']
                    if check_mod(obj, "read", sessionid, app, key):
                        result.append(obj)
            
        response['result'] = result
    
    return HttpResponse(json.dumps(response) + "\n", content_type="application/json")


def validate_session(sessionid, app, key):
    import requests
 
    res = requests.get(USER_SESSION_URL + 'validate_session/?sessionId=' + sessionid, headers={'X-Voolks-App-Id': app, 'X-Voolks-Api-Key': key},verify=False)
    
    return json.loads(res.text)

def check_mod(obj, action, sessionid, app, key):
    parsed_data = {}
    data = obj
    for k in data:
        if k.find("_") == 0:
            if k == "_mod":
                mod = data[k]
                session = validate_session(sessionid, app, key)
                if not "userid" in session:
                    return False
                else:
                    try:
                        if mod[str(session['userid'])] != action and mod[str(session['userid'])] != "*":
                            return False
                    #except:
                    #        return False
    return True

@csrf_exempt
@HttpOptionsDecorator
@VoolksAPIAuthRequired
def classes_get_one(request, class_name, obj_id):
    
    response = {}
    database_name = "test"
    connection = Connection()
    db = connection[database_name]
    sessionid = request.GET.get("sessionid", "")

    app = request.META.get('HTTP_X_VOOLKS_APP_ID')
    if not app:
        app = request.GET.get('VoolksAppId','')


    key = request.META.get('HTTP_X_VOOLKS_API_KEY')
    if not key:
        key = request.GET.get('VoolksApiKey','')
    
    instance = db[app + "-" + class_name]

    parsed_data = {}
        
    if obj_id and obj_id is not "":

        obj = instance.find_one({'_id': ObjectId(obj_id)})
        obj['id'] = obj_id

        # Delete
        if request.META["REQUEST_METHOD"] == "DELETE":
            if check_mod(obj, "delete", sessionid, app, key):
                instance.remove({'_id': ObjectId(obj_id)})

        # Update
        elif request.META["REQUEST_METHOD"] == "PUT":
            if check_mod(obj, "update", sessionid, app, key):
                data = request.read()
                parsed_data = json.loads(data)
                parsed_data['updatedAt'] = str(datetime.now())
                obj = instance.update({'_id':ObjectId(obj_id)}, parsed_data)


        else:
        # Get by id
            if check_mod(obj, "read", sessionid, app, key):
                del obj["_id"]
                parsed_data = obj
                
        return HttpResponse(json.dumps(parsed_data) + "\n", content_type="application/json")
        
    else:
        return HttpResponse(json.dumps({}), content_type="application/json")
        
    
    
