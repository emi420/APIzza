import string
import os.path
import copy
import requests
import mimetypes
from file import settings
from django.http import HttpResponseRedirect, HttpResponse
from decorators import HttpOptionsDecorator, VoolksAPIAuthRequired
from django.views.decorators.csrf import csrf_exempt


def get_api_credentials(request):
    ''' Get app id and api key '''

    app = request.META.get('HTTP_X_VOOLKS_APP_ID')
    key = request.META.get('HTTP_X_VOOLKS_API_KEY')

    if not key:
        try:
            key = request.GET.get('VoolksApiKey')
            app = request.GET.get('VoolksAppId')
        except(e):
            pass

    
    return (app, key)


@csrf_exempt
@HttpOptionsDecorator
@VoolksAPIAuthRequired
def get(request, name):
    (app, key) = get_api_credentials(request)
    try:
        path = settings.MEDIA_ROOT + app + "-" + key + "-" + name 
        dest = open(path, 'r')
        fileContent = dest.read()
        dest.close()
        mimeType = mimetypes.guess_type(path)
        if mimeType == (None,None):
               mimeType = "text/plain"
        return HttpResponse(fileContent,  content_type=mimeType)
    except:
        return HttpResponse("FILE NOT FOUND")

@csrf_exempt
@HttpOptionsDecorator
@VoolksAPIAuthRequired
def delete(request, name):
    (app, key) = get_api_credentials(request)
    try:
        path = settings.MEDIA_ROOT + app + "-" + key + "-" + name
        os.remove(path)
        return HttpResponse("OK")
    except:
        return HttpResponse("ERROR")
    
@csrf_exempt
@HttpOptionsDecorator
@VoolksAPIAuthRequired
def create(request):
    
    (app, key) = get_api_credentials(request)

    if len(request.FILES) < 1:
        return HttpResponse("NO_FILES_FOUND")

    else:
        fileKey = request.FILES.keys()[0]
        file = request.FILES[fileKey]

        # Check file size
        if file.size > settings.MEDIA_MAX_FILE_SIZE:
            return HttpResponse("FILE_SIZE_EXCEEDED")

        # Check file extension
        if file.name.split(".")[-1].lower() not in settings.MEDIA_PERMITTED_EXTENSIONS:
            return HttpResponse("FILE_EXTENSION_NOT_PERMITTED")

        path = settings.MEDIA_ROOT + app + "-" + key + "-" + file.name
        dest = open(path, 'w+')

        if file.multiple_chunks:
            for c in file.chunks():
                dest.write(c)
        else:
            dest.write(file.read())
        dest.close()
        return HttpResponseRedirect("/" + file.name + "?VoolksAppId=" + app + "&VoolksApiKey=" + key) 

@csrf_exempt
@HttpOptionsDecorator
@VoolksAPIAuthRequired
def createBase64(request):
    
    (app, key) = get_api_credentials(request)

    #import pdb; pdb.set_trace();

    if len(request.POST) < 1:
        return HttpResponse("NO_FILES_FOUND")
    else:
        fileKey = request.POST.keys()[0]

        # Check file size
        if len(request.POST[fileKey]) > settings.MEDIA_MAX_FILE_SIZE:
            return HttpResponse("FILE_SIZE_EXCEEDED")
        
        filename = fileKey

        # Check file extension
        if filename.split(".")[-1].lower() not in settings.MEDIA_PERMITTED_EXTENSIONS:
            return HttpResponse("FILE_EXTENSION_NOT_PERMITTED")

        path = settings.MEDIA_ROOT + app + "-" + key + "-" + filename
        dest = open(path, 'w+')
        
        try:
            dest.write(request.POST[fileKey][22:].decode('base64'))
        except:
            dest.write(request.POST[fileKey].decode('base64'))

        dest.close()
        #return HttpResponse("OK")
        return HttpResponse(filename)

    return HttpResponse("ERROR")
