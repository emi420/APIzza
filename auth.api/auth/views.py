import json
from decorators import HttpOptionsDecorator, VoolksAPIAuthRequired
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.sessions.backends.db import SessionStore

def signup(request):
   ''' Register user '''

   response = {}
   username = request.GET.get('username','')
   password = request.GET.get('password','')
            
   # Error codes if missing data

   if username == '':
      response['code'] = 54
      response['text'] = "Username not provided"
      return HttpResponse(json.dumps(response) + "\n", content_type="application/json")

   elif password == '':
      response['code'] = 55
      response['text'] = "Password not provided"
      return HttpResponse(json.dumps(response) + "\n", content_type="application/json")

   else:

     # Create user
      
     user = User.objects.create_user(username, username, password)
     
     if user is not None:

         # Save session
         
         s = SessionStore()
         s['ip_address'] = request.META['REMOTE_ADDR'] 
         s['id'] = user.pk
         s.save()
         session_id = s.session_key

         # Build response
         
         response['sessionId'] = session_id
         response['username'] = user.username
         response['id'] = user.pk

         return HttpResponse(json.dumps(response) + "\n", content_type="application/json")

     else:

         # Can't create user
         
         response['code'] = 56
         response['text'] = "Can't create user"
         return HttpResponse(json.dumps(response) + "\n", content_type="application/json")



@HttpOptionsDecorator
@VoolksAPIAuthRequired
def login(request):
   ''' Authenticate user '''
    
   response = {}
   username = request.GET.get('username','')
   password = request.GET.get('password','')
            
   # Error codes
   
   if username == '':
      response['code'] = 44
      response['text'] = "Username not provided"
      return HttpResponse(json.dumps(response) + "\n", content_type="application/json")

   elif password == '':
      response['code'] = 45
      response['text'] = "Password not provided"
      return HttpResponse(json.dumps(response) + "\n", content_type="application/json")

   else:
      
     # Auhenticate user
     
     user = authenticate(username=username, password=password)
     
     if user is not None:

         # Save session
         
         s = SessionStore()
         s['ip_address'] = request.META['REMOTE_ADDR'] 
         s['id'] = user.pk
         s.save()
         session_id = s.session_key

         # Build response
         
         response['sessionId'] = session_id
         response['username'] = user.username
         response['id'] = user.pk

         return HttpResponse(json.dumps(response) + "\n", content_type="application/json")

     else:

         # Can't authenticate
         
         response['code'] = 46
         response['text'] = "Invalid username or password"
         return HttpResponse(json.dumps(response) + "\n", content_type="application/json")


@HttpOptionsDecorator
@VoolksAPIAuthRequired
def validate_session(request, session_id):
   ''' Check if user session if valid '''

   response = {}
   s = SessionStore(session_key=session_id)
   
   # FIXME CHECK
   if 'ip_address' in s: # and s['ip_address'] == request.META['REMOTE_ADDR'] :
       response['userid'] = s['id']
       response['code'] = 1
   else:
       response['code'] = 0
       
   return HttpResponse(json.dumps(response) + "\n", content_type="application/json")
   
   
  