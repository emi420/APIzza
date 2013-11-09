import json
from decorators import HttpOptionsDecorator, VoolksAPIAuthRequired
from django.http import HttpResponse
from pymongo import Connection
from bson.objectid import ObjectId
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

@HttpOptionsDecorator
@VoolksAPIAuthRequired
@csrf_exempt
def classes(request, class_name):

    response = {}
    database_name = "test"
    connection = Connection()
    db = connection[database_name]
    instance = db[class_name]
    
    # Create 

    if len(request.POST.items()) > 0:

        data = request.POST.items()[0][0]
        parsed_data = json.loads(data)
        parsed_data['createdAt'] = str(datetime.now())
        obj = instance.insert(parsed_data)
        response['id'] = str(obj)
    
    else:
        
        # Get all
        
        cur = instance.find()
        result = []
        
        for i in range(0, cur.count()):
            obj = cur.next()
            obj['id'] = str(obj['_id'])
            del obj['_id']
            result.append(obj)
            
        response['result'] = result
    
    return HttpResponse(json.dumps(response), content_type="application/json")

@HttpOptionsDecorator
@VoolksAPIAuthRequired
def classes_get_one(request, class_name, obj_id):
    
    response = {}
    database_name = "test"
    connection = Connection()
    db = connection[database_name]
    instance = db[class_name]

    obj = instance.find_one({'_id': ObjectId(obj_id)})
    obj['id'] = obj_id
    del obj['_id']
    
    return HttpResponse(json.dumps(obj), content_type="application/json")
    
    