import json
from decorators import HttpOptionsDecorator, VoolksAPIAuthRequired
from django.http import HttpResponse
from pymongo import Connection
from bson.objectid import ObjectId
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

USER_SESSION_URL = "http://localhost:8000/users/"

@csrf_exempt
@HttpOptionsDecorator
@VoolksAPIAuthRequired
def classes(request, class_name):

    response = {}
    database_name = "test"
    connection = Connection()
    db = connection[database_name]
    
    app = request.META.get('HTTP_X_VOOLKS_APP_ID')
    if not app:
        app = request.GET.get('VoolksAppId','')
    
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
                instance.remove(json.loads(request.GET["where"]))
                delete = True
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
            # Get all
            if request.META["REQUEST_METHOD"] == "DELETE":
                delete = True
                instance.remove()
            elif "count" in request.GET and request.GET["count"] == "true":
                cur = instance.find().count()
            else:
                cur = instance.find()

        
        result = []
        
        if "count" in request.GET and request.GET["count"] == "true":
            result = {}
            result["count"] = cur
        else:
            if delete is not True:
                for i in range(0, cur.count()):
                    obj = cur.next()
                    obj['id'] = str(obj['_id'])
                    del obj['_id']
                    result.append(obj)
            
        response['result'] = result
    
    return HttpResponse(json.dumps(response) + "\n", content_type="application/json")


def validate_session(sessionid, app, key):
    import requests
 
    res = requests.get(USER_SESSION_URL + 'validate_session/?sessionId=' + sessionid, headers={'X-Voolks-App-Id': app, 'X-Voolks-Api-Key': key},verify=False)
    
    return json.loads(res.text)


@csrf_exempt
@HttpOptionsDecorator
@VoolksAPIAuthRequired
def classes_get_one(request, class_name, obj_id):
    
    response = {}
    database_name = "test"
    connection = Connection()
    db = connection[database_name]

    app = request.META.get('HTTP_X_VOOLKS_APP_ID')
    if not app:
        app = request.GET.get('VoolksAppId','')


    key = request.META.get('HTTP_X_VOOLKS_API_KEY')
    if not key:
        key = request.GET.get('VoolksApiKey','')
    
    instance = db[app + "-" + class_name]

    parsed_data = {}
    
    if obj_id and obj_id is not "":

        # Delete
        if request.META["REQUEST_METHOD"] == "DELETE":
            instance.remove({'_id': ObjectId(obj_id)})

        # Update
        elif request.META["REQUEST_METHOD"] == "PUT":
            data = request.read()
            parsed_data = json.loads(data)
            parsed_data['updatedAt'] = str(datetime.now())
            obj = instance.update({'_id':ObjectId(obj_id)}, parsed_data)
            parsed_data['id'] = obj_id


        else:
        # Get by id
        
            obj = instance.find_one({'_id': ObjectId(obj_id)})
            if obj:
                obj['id'] = obj_id
                data = obj;
                for k in data:
                    if k.find("_") != 0:
                        parsed_data[k] = data[k]
                    else:
                        # Move this code to a 'check_mod' method
                        if k == "_mod":
                            mod = data[k]
                            sessionid = request.GET.get("sessionid", "")
                            session = validate_session(sessionid, app, key)
                            if not "userid" in session:
                                parsed_data = {}                                
                                break
                            else:
                                try:
                                    if mod[str(session['userid'])] != "read":
                                        parsed_data = {}                                
                                        break
                                except:
                                        parsed_data = {}                                
                                        break
                                
                del obj['_id']

        return HttpResponse(json.dumps(parsed_data) + "\n", content_type="application/json")
        
    else:
        return HttpResponse(json.dumps({}), content_type="application/json")
        
    
    
