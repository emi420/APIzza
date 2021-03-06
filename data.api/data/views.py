import json
from decorators import HttpOptionsDecorator, VoolksAPIAuthRequired
from django.http import HttpResponse
from pymongo import Connection
from bson.objectid import ObjectId
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import re


USER_SESSION_URL = "http://localhost:8000/"
DATABASE_NAME = "test"

# xxx
# For checking for specific permission when no session is provided
CHK_SP_PERM_AUTH_USER = "validate_data_api"
CHK_SP_PERM_AUTH_PASSWORD = "validate_data_api_123"


def get_api_credentials(request):
    ''' Get app id and api key '''

    app = request.META.get('HTTP_X_VOOLKS_APP_ID')
    key = request.META.get('HTTP_X_VOOLKS_API_KEY')
    
    return (app, key)
    

@csrf_exempt
@HttpOptionsDecorator
@VoolksAPIAuthRequired
def classes(request, class_name):
    ''' Get, Delete, Count or Update multiple items'''
    ''' Create a single item '''

    response = {}
    sessionid = request.META.get('HTTP_X_VOOLKS_SESSION_ID')
    (app, key) = get_api_credentials(request)
    connection = Connection()
    db = connection[DATABASE_NAME]    
    instance = db[app + "-" + class_name]
    skip = 0
    limit = 0
    cur = None
    count = 0
    result = []
    request_delete = request.META["REQUEST_METHOD"] == "DELETE"
    request_post = request.META["REQUEST_METHOD"] == "POST"
    request_content_type_json = request.META.get('CONTENT_TYPE') == "application/json; charset=UTF-8"
    queryIsList = False
    
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
        
        '''try:
            parsed_data = json.loads(data)
        except:
            return HttpResponse(json.dumps({"error":"Invalid JSON","code":"533"}) + "\n", content_type="application/json")
        '''

        # Validate field names (only letters, numbers and underscores are permitted)
        for tmp_field_name in parsed_data.keys():
            if not re.match("^[a-zA-Z0-9_]*$", tmp_field_name):
                return HttpResponse(json.dumps({"error":"Invalid field name","code":"61"}) + "\n", content_type="application/json")

        parsed_data['createdAt'] = str(datetime.now())
        obj = instance.insert(parsed_data)
        response['id'] = str(obj)
        
        if "_permissions" in parsed_data:
            
            session = validate_session(sessionid, app, key)
            if not "userid" in session:
                return HttpResponse(json.dumps({"error":"Invalid session","code":"53"}) + "\n", content_type="application/json")
            else:
                userid = str(session['userid'])
                db_objid = ""
                db_user = ""
                db_user_permissions = ""
                db_other_permissions = ""
                # for user in parsed_data['_permissions'].iterkeys():
                    # if user == "*":
                        # db_other_permissions = json.dumps(parsed_data['_permissions'][user])
                    # else:
                        # db_user = user
                        # db_user_permissions = json.dumps(parsed_data['_permissions'][user])
                db_objid = str(obj)
                data_permissions = parsed_data['_permissions']
                
                create_response = create_object_permissions(sessionid, app, key, db_objid, data_permissions)
                
    else:

        # Get data

        if "where" in request.GET:
            query = json.loads(request.GET["where"])
            if type(query) is dict:
                if "_id" in query:       
                    if type(query['_id']) is dict:
                        if "$in" in query['_id']: 
                            in_list = []
                            for tmp_id in query['_id']['$in']:
                                in_list.append(ObjectId(str(tmp_id)))
                            query['_id']['$in'] = in_list
                    else:
                        query["_id"] = ObjectId(str(query["_id"]))
                cur = instance.find(query)
            elif type(query) is list:
                cur = instance.find(query[0],query[1]) 
                query1 = query[1]
                query = query[0]

                queryIsList = True   

        else:
            query = {}

        if "sort" in request.GET:
            # * http://docs.mongodb.org/manual/reference/method/cursor.sort/
            # * http://stackoverflow.com/questions/10242149/sorting-with-mongodb-and-python
            # sort_param = json.loads(request.GET["sort"])
            sort_param = []
            for k, v in json.loads(request.GET["sort"]).iteritems():
                sort_param.insert(0, (k, v))
        else:
            # sort_param = {"$natural": 1}
            sort_param = [("$natural", 1)]

        # Make query for permissions
        
        if not sessionid:
            query["$or"] = [
                {"_mod":{"$exists": False}},
            ]

        else:

            session = validate_session(sessionid, app, key)
            if not "userid" in session:
                return HttpResponse(json.dumps({"error":"Invalid session","code":"53"}) + "\n", content_type="application/json")
            else:
                userid = str(session['userid'])

            if request_delete:

                query["$or"] = [
                    {"_mod":{"$exists": False}},
                    {"_mod":{userid:"write"}}
                ]
                
            else:

                query["$or"] = [
                    {"_mod":{"$exists": False}},
                    {"_mod":{userid:"read"}},
                    {"_mod":{userid:"write"}}
                ]
                
                                
        # Get
        
        if not request_delete:

            if "skip" in request.GET:
                skip = int(request.GET.get("skip"))

            if not "limit" in request.GET:
                if not queryIsList:
                    cur = instance.find(query).sort(sort_param).skip(skip)
                else:
                    cur = instance.find(query,query1).sort(sort_param).skip(skip)
            else:
               limit = int(request.GET.get("limit"))
               if not queryIsList:
                    cur = instance.find(query).sort(sort_param).skip(skip).limit(limit)
               else:
                    cur = instance.find(query,query1).sort(sort_param).skip(skip).limit(limit)

        # Delete

        else:
            instance.remove(query)
                
        # Count
        
        if cur:
            count = cur.count()
            if limit and count > limit:
                count = limit
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
    res = requests.get(USER_SESSION_URL + 'validate/' + sessionid + '/', headers={'X-Voolks-App-Id': app, 'X-Voolks-Api-Key': key},verify=False)    
    response = json.loads(res.text)
    return response

def create_object_permissions(sessionid, app, key, obj_id, data_permissions):
    ''' Create object permissions using an external API (auth.api)'''

    import requests    
    headers = {"Content-Type": "application/x-www-form-urlencoded", "X-Voolks-Session-Id": sessionid, "X-Voolks-App-Id": app, "X-Voolks-Api-Key": key }
    url = USER_SESSION_URL + "permissions/"
    data = { obj_id: data_permissions}
    params = {}
    res = requests.post(url, params=params, data=json.dumps(data), headers=headers)
    
    response = json.loads(res.text)
    return response
    
    
def get_object_permissions(sessionid, app, key, obj_id):
    ''' Check if object have specific permissions using an external API (auth.api)'''

    import requests
    res = requests.get(USER_SESSION_URL + 'permissions/?objid=' + obj_id, headers={'X-Voolks-Session-Id': sessionid, 'X-Voolks-App-Id': app, 'X-Voolks-Api-Key': key},verify=False)
    response = json.loads(res.text)
    return response

# xxx
def get_tmp_session(app, key):
    ''' Get temporary session (for checking existence of permissions) using an external API (auth.api)'''

    import requests
    res = requests.get(USER_SESSION_URL + "login/?username=" + CHK_SP_PERM_AUTH_USER + "&password=" + CHK_SP_PERM_AUTH_PASSWORD, headers={'X-Voolks-App-Id': app, 'X-Voolks-Api-Key': key},verify=False)
    response = json.loads(res.text)
    return response


@csrf_exempt
@HttpOptionsDecorator
@VoolksAPIAuthRequired
def classes_get_one(request, class_name, obj_id):
    ''' Get, Delete or Update one item'''

    response = {}
    parsed_data = {}
    sessionid = request.META.get('HTTP_X_VOOLKS_SESSION_ID')
    (app, key) = get_api_credentials(request)
    connection = Connection()
    db = connection[DATABASE_NAME]
    instance = db[app + "-" + class_name]
    obj = None
    userid = None
    request_delete = request.META["REQUEST_METHOD"] == "DELETE"
    request_put = request.META["REQUEST_METHOD"] == "PUT"
    

    if obj_id and obj_id is not "":

        # Check if object has specific permissions
        if not sessionid:
            # xxx
            # No session, get temporary one for checking if specific permissions exist
            tmp_session = get_tmp_session(app, key)
            tmp_session_sessionid = tmp_session["sessionId"]
            tmp_session_userid = tmp_session["id"]
            obj_perm = get_object_permissions(tmp_session_sessionid, app, key, obj_id)
            if obj_perm["code"] == 1 or obj_perm["code"] == 500:
                return HttpResponse(json.dumps({"error":"Permission denied.","code":"45"}) + "\n", content_type="application/json")

        else:
            # Check if this user has the right specific permissions
            obj_perm = get_object_permissions(sessionid, app, key, obj_id)
            if obj_perm["code"] == 1:
                # Object has specific permissions, check if user has the rights to access it
                session = validate_session(sessionid, app, key)
                if not "userid" in session:
                    return HttpResponse(json.dumps({"error":"Invalid session","code":"53"}) + "\n", content_type="application/json")
                else:
                    userid = str(session['userid'])
                    if request_delete or request_put:
                        if userid not in obj_perm["permissions"][obj_id] and obj_perm["permissions"][obj_id]["*"]["write"] == "false":
                            return HttpResponse(json.dumps({"error":"Permission denied.","code":"47"}) + "\n", content_type="application/json")
                    else:
                        if userid not in obj_perm["permissions"][obj_id] and obj_perm["permissions"][obj_id]["*"]["read"] == "false":
                            return HttpResponse(json.dumps({"error":"Permission denied.","code":"46"}) + "\n", content_type="application/json")

        query = {}
        query["_id"] = ObjectId(obj_id)

        # Make query for permissions
        
        if not sessionid:

            query["$or"] = [
                {"_mod":{"$exists": False}},
            ]

        else:

            session = validate_session(sessionid, app, key)
            if not "userid" in session:
                return HttpResponse(json.dumps({"error":"Invalid session","code":"53"}) + "\n", content_type="application/json")
            else:
                userid = str(session['userid'])

            if request_delete or request_put:

                query["$or"] = [
                    {"_mod":{"$exists": False}},
                    {"_mod":{userid:"write"}}
                ]
                
            else:

                query["$or"] = [
                    {"_mod":{"$exists": False}},
                    {"_mod":{userid:"read"}},
                    {"_mod":{userid:"write"}}
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
                parsed_data['createdAt'] = obj['createdAt']
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
        return HttpResponse(json.dumps({}) + "\n", content_type="application/json")
        
    
    
