import string
import os.path
import copy
import requests
from file import settings
from django.http import HttpResponseRedirect, HttpResponse
from decorators import HttpOptionsDecorator, VoolksAPIAuthRequired
from django.views.decorators.csrf import csrf_exempt


def get_api_credentials(request):
    ''' Get app id and api key '''

    app = request.META.get('HTTP_X_VOOLKS_APP_ID')
    key = request.META.get('HTTP_X_VOOLKS_API_KEY')
    
    return (app, key)
    
@csrf_exempt
@HttpOptionsDecorator
@VoolksAPIAuthRequired
def create(request, id):
    
    (app, key) = get_api_credentials(request)

    if len(request.FILES) < 1:
        return HttpResponse("NO_FILES_FOUND")

    else:
        fileKey = request.FILES.keys()[0]
        file = request.FILES[fileKey]
        path = settings.MEDIA_ROOT + app + "-" + key + "-" + file.name
        dest = open(path, 'w+')

        if file.multiple_chunks:
            for c in file.chunks():
                dest.write(c)
        else:
            dest.write(file.read())
        dest.close()
        return HttpResponse("OK")
        

@csrf_exempt
@HttpOptionsDecorator
@VoolksAPIAuthRequired
def createBase64(request, id):
    
    (app, key) = get_api_credentials(request)

    if len(request.POST) < 1:
        return HttpResponse("NO_FILES_FOUND")
    else:
        fileKey = request.POST.keys()[0]

        filename = fileid + ".png"
        path = settings.MEDIA_ROOT + app + "-" + key + "-" + filename
        dest = open(path, 'w+')
        
        dest.write(request.POST[fileKey].decode('base64'))
        dest.close()
        return HttpResponse("OK")

    return HttpResponse("ERROR")