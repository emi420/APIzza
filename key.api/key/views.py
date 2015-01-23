import json
from django.http import HttpResponse

from key.models import App, AppPermission

from django.views.decorators.csrf import csrf_exempt

def check_key(request):
    ''' Check if a key is valid '''

    app = request.META.get('HTTP_X_VOOLKS_APP_ID')
    key = request.META.get('HTTP_X_VOOLKS_API_KEY')
    
    # If parameters missing, return error

    if not app or not key:
        return HttpResponse(json.dumps({'code':1,'text': 'Parameters not found'}),status=400)

    # Get and return App object

    appObj = App.objects.get(id_aplicacion=app,api_key=key)
    
    try:
        permissionsObj = AppPermission.objects.get(objid=app)
        permissions = permissionsObj.permissions
    except:
        permissions = "PUT, DELETE, POST, GET, OPTIONS"

    return HttpResponse(json.dumps({"domain": appObj.dominio, "permissions": permissions}),status=200)

@csrf_exempt    
def create_key(request):
    ''' Create key '''

    response = {}
    
    request_content_type_json = request.META.get('CONTENT_TYPE') == "application/json; charset=UTF-8"

    if request.META["REQUEST_METHOD"] == "POST":
    
        # Create key
        data = []
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
        id_aplication = parsed_data["id_aplication"]  
        api_key = parsed_data["api_key"]
        name = parsed_data["name"]
        domine = parsed_data["domine"]
        permissions = parsed_data["permission"]

        # Error codes if missing data
        
        if id_aplication == '':
          response['code'] = 50
          response['text'] = "Id application not provided"
          return HttpResponse(json.dumps(response) + "\n", content_type="application/json")
        
        if api_key == '':
          response['code'] = 51
          response['text'] = "Api key not provided"
          return HttpResponse(json.dumps(response) + "\n", content_type="application/json")

        if name == '':
          response['code'] = 52
          response['text'] = "Name not provided"
          return HttpResponse(json.dumps(response) + "\n", content_type="application/json")

        if domine == '':
          response['code'] = 53
          response['text'] = "Domine not provided"
          return HttpResponse(json.dumps(response) + "\n", content_type="application/json")

        # Create key
        
        try:
            # Build response
            appObj = App.objects.create(id_aplicacion=id_aplication,api_key=api_key,nombre=name,dominio=domine)
            if permissions != '':
                AppPermission.objects.create(objid=appObj.id,permissions=permissions)
            response['id'] = str(appObj.id)
        except:
            # Can't create key
            response['code'] = 54
            response['text'] = "Can't create key"
            return HttpResponse(json.dumps(response) + "\n", content_type="application/json")
        
    return HttpResponse(json.dumps(response) + "\n", content_type="application/json")

@csrf_exempt    
def delete(request):
    ''' Delete key '''
    
    response = {}

    if request.META["REQUEST_METHOD"] == "DELETE":
        apiname = request.GET.get('name','')
        
        # Error codes if missing data
        
        if apiname == '':
            response['code'] = 57
            response['text'] = "Name not provided"
            return HttpResponse(json.dumps(response) + "\n", content_type="application/json")
       
        # Delete key
       
        try:
            appObj = App.objects.get(nombre=apiname)
            AppPermission.objects.filter(objid=appObj.id).delete()
            App.objects.filter(nombre=apiname).delete()
        except:
            # Can't delete key
            
            response['code'] = 58
            response['text'] = "Can't delete key"
            return HttpResponse(json.dumps(response) + "\n", content_type="application/json")

        # Build response

        response['code'] = 1
        response['text'] = "Key deleted"
        
    return HttpResponse(json.dumps(response) + "\n", content_type="application/json")