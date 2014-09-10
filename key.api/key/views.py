import json
from django.http import HttpResponse

from key.models import App, AppPermission

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
        permissions = ""

    return HttpResponse(json.dumps({"domain": appObj.dominio, "permissions": permissions}),status=200)

    
