import json
from django.http import HttpResponse

from key.models import App

def check_key(request):
    ''' Check if a key is valid '''

    app = request.META.get('HTTP_X_VOOLKS_APP_ID')
    key = request.META.get('HTTP_X_VOOLKS_API_KEY')
    
    # If parameters missing, return error

    if not app or not key:
        return HttpResponse(json.dumps({'code':1,'text': 'Parameters not found'}),status=400)

    # Get and return App object

    app = App.objects.get(id_aplicacion=app,api_key=key)
    
    try:
        permissionsObj = AppPermissions.objects.get(objid=app)
        permissions = permissionsObj.permissions
    except:
        permissions = "PUT, DELETE, POST, GET, OPTIONS"

    return HttpResponse(json.dumps({"domain": app.dominio, "permissions": permissions}),status=200)

    