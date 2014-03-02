import json
from decorators import HttpOptionsDecorator, VoolksAPIAuthRequired
from django.http import HttpResponse
from pymongo import Connection
from bson.objectid import ObjectId
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime


@csrf_exempt
@HttpOptionsDecorator
@VoolksAPIAuthRequired
def classes(request, class_name):

    response = {}
    database_name = "test"
    connection = Connection()
    db = connection[database_name]
    instance = db[class_name]
    delete = False
    
    
    if request.META["REQUEST_METHOD"] == "POST":
        
        # Create 
        data = request.POST.items()[0][0]
        
        # FIXME CHECK
        #try:
        parsed_data = json.loads(data)
        #except:
        #    import pdb; pdb.set_trace();
        #    parsed_data = json.loads("{" + data + "}")

        parsed_data['createdAt'] = str(datetime.now())
        obj = instance.insert(parsed_data)
        response['id'] = str(obj)
        
    else:
        
        if "where" in request.GET:
            # Delete
            if request.META["REQUEST_METHOD"] == "DELETE":
                instance.remove(json.loads(request.GET["where"]))
                delete = True
            elif request.GET["count"] == "True":
                cur = instance.find(json.loads(request.GET["where"]).count())
            else:
            # Where
                cur = instance.find(json.loads(request.GET["where"]))
            
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
    
    return HttpResponse(json.dumps(response), content_type="application/json")

@csrf_exempt
@HttpOptionsDecorator
@VoolksAPIAuthRequired
def classes_get_one(request, class_name, obj_id):
    
    response = {}
    database_name = "test"
    connection = Connection()
    db = connection[database_name]
    instance = db[class_name]
    parsed_data = {}
    
    if obj_id and obj_id is not "":

        # Get by id
        obj = instance.find_one({'_id': ObjectId(obj_id)})
        obj['id'] = obj_id
        del obj['_id']

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

        return HttpResponse(json.dumps(parsed_data), content_type="application/json")
        
    else:
        return HttpResponse(json.dumps({}), content_type="application/json")
        
    
    