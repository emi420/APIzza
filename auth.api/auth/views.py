import json
from decorators import HttpOptionsDecorator, VoolksAPIAuthRequired
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.sessions.backends.db import SessionStore
from auth.models import AuthPermission

@HttpOptionsDecorator
@VoolksAPIAuthRequired
def signup(request):
   ''' Register user '''

   response = {}
   
   # get app id
   # username = request.GET.get('username','') + app id
   
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
   
   
@HttpOptionsDecorator
@VoolksAPIAuthRequired
def permissions(request, session_id):
    ''' Manage user permissions for objects '''

    response = {}
    s = SessionStore(session_key=session_id)

    # Check for valid session
    if 'id' in s:
        # Create permissions for object?
        if request.META["REQUEST_METHOD"] == "POST":
            data = request.POST.items()[0][0]
            parsed_data = json.loads(data)
            db_objid = ""
            db_user = ""
            db_user_permissions = ""
            db_other_permissions = ""
            for objid in parsed_data.iterkeys():
                db_objid = objid
                for user in parsed_data[objid].iterkeys():
                    if user == "*":
                        db_other_permissions = str(parsed_data[objid][user]).replace("{u'", "{'").replace(", u'", ", '").replace(": u'", ": '")
                    else:
                        db_user = user
                        db_user_permissions = str(parsed_data[objid][user]).replace("{u'", "{'").replace(", u'", ", '").replace(": u'", ": '")

            #response['debug'] = " db_objid = " + db_objid + " db_user = " + db_user + " db_user_permissions = " + db_user_permissions + " db_other_permissions = " + db_other_permissions
            
            # TODO: Restrictions & validations...

            try:
                AuthPermission.objects.get(objid=db_objid, user=db_user)
                AuthPermission.objects.update(objid=db_objid, user=db_user, user_permissions=db_user_permissions, other_permissions=db_other_permissions)
            except AuthPermission.DoesNotExist:
                AuthPermission.objects.create(objid=db_objid, user=db_user, user_permissions=db_user_permissions, other_permissions=db_other_permissions)

            response['code'] = 1
        else:
            response['code'] = 0
    else:
        response['code'] = 0

    return HttpResponse(json.dumps(response) + "\n", content_type="application/json")
  
