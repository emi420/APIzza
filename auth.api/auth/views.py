import json
import urllib
from decorators import HttpOptionsDecorator, VoolksAPIAuthRequired
from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
from django.contrib.sessions.backends.db import SessionStore
from auth.models import AuthPermission
import re
import md5
import random
import string

RESET_SECRET_KEY = "reset_secret_key"

def get_api_credentials(request):
    ''' Get app id and api key '''

    app = request.META.get('HTTP_X_VOOLKS_APP_ID')
    key = request.META.get('HTTP_X_VOOLKS_API_KEY')
    
    return (app, key)


@HttpOptionsDecorator
@VoolksAPIAuthRequired
def signup(request):
   ''' Register user '''

   response = {}

   (app, key) = get_api_credentials(request)
   
   request_post = request.META["REQUEST_METHOD"] == "POST"
   request_content_type_json = request.META.get('CONTENT_TYPE') == "application/json; charset=UTF-8"
   
   if request_post:
        if request_content_type_json:
            data = "{"
            params = dict([p.split('=') for p in request.body.split('&')])
            for key2 in params: 
                data = data + '"' + key2 + '":"' +params[key2] + '",'
            data = data + "}"
            data = data.replace(",}","}")
            parsed_data = json.loads(data)
            username = parsed_data["username"]
            password = parsed_data["password"]
        else:
            data = request.POST.items()[0][0]
            parsed_data = json.loads(data)
            username = parsed_data["username"]
            password = parsed_data["password"]
                       
   else:
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
      
      lenPassword = len(str(password))
     
      # Error codes if missing data 

      try:
         userExists = User.objects.get(username=app + "-" + key + "-" + username)
         response['code'] = 62
         response['text'] = "Username exists"
         return HttpResponse(json.dumps(response) + "\n", content_type="application/json")
      except:
         userExists = ''
            
      if lenPassword < 8:
         response['code'] = 59
         response['text'] = "Password too short"
         return HttpResponse(json.dumps(response) + "\n", content_type="application/json")
      elif not re.search('[0-9]+', str(password)):
         response['code'] = 60
         response['text'] = "Password must contain at least one number"
         return HttpResponse(json.dumps(response) + "\n", content_type="application/json")
      elif not re.search('[a-zA-Z]+', str(password)):
         response['code'] = 61
         response['text'] = "Password must contain at least one letter"
         return HttpResponse(json.dumps(response) + "\n", content_type="application/json")
      else:

         # Create user
          
         #user = User.objects.create_user(username, username, password)
         user = User.objects.create_user(app + "-" + key + "-" + username, username, password)

         if user is not None:

             # Save session
             
             s = SessionStore()
             s['ip_address'] = request.META['REMOTE_ADDR'] 
             s['id'] = user.pk
             s.save()
             session_id = s.session_key

             # Build response
             
             response['sessionId'] = session_id
             response['username'] = user.username.replace(app + "-" + key + "-","")
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

   (app, key) = get_api_credentials(request)

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
     
     user = authenticate(username=app + "-" + key + "-" + username, password=password)
     
     if user is not None:

         # Save session
         
         s = SessionStore()
         s['ip_address'] = request.META['REMOTE_ADDR'] 
         s['id'] = user.pk
         s.save()
         session_id = s.session_key

         # Build response
         
         response['sessionId'] = session_id
         response['username'] = user.username.replace(app + "-" + key + "-","")
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
def permissions(request):
    ''' Manage user permissions for objects '''

    response = {}

    session_id = request.META.get('HTTP_X_VOOLKS_SESSION_ID')
    request_content_type_json = request.META.get('CONTENT_TYPE') == "application/json; charset=UTF-8"
    s = SessionStore(session_key=session_id)

    # Check for valid session
    if 'id' in s:
        # Create/update permissions for object
        if request.META["REQUEST_METHOD"] == "POST" or request.META["REQUEST_METHOD"] == "PUT":
            data = []
            if request.META["REQUEST_METHOD"] == "POST":
                if request_content_type_json:
                    decode = urllib.unquote(request.body)
                    decode = decode.replace("[","|")
                    decode = decode.replace("]","|")
                    decode = decode.replace("=","")
                    sp = decode.split('&')
                    sp0 = sp[0].split('|')
                    sp1 = sp[1].split('|')
                    sp2 = sp[2].split('|')
                    sp3 = sp[3].split('|')
                    
                    data = '{'
                    data = data + '"' + sp0[0] + '":{'
                    data = data + '"' + sp0[1] + '":{' + '"' + sp0[3] + '":' + '"' + sp0[4] + '",' + '"' + sp1[3] + '":' + '"' + sp1[4] + '"' + '},'
                    data = data + '"' + sp3[1] + '":{' + '"' + sp2[3] + '":' + '"' + sp2[4] + '",' + '"' + sp3[3] + '":' + '"' + sp3[4] + '"' + '}'
                    data = data + '}'
                    data = data + '}'
                else:
                    data = request.POST.items()[0][0]
            else:
                data = request.read()
            parsed_data = json.loads(data)
            db_objid = ""
            db_user = ""
            db_user_permissions = ""
            db_other_permissions = ""
            for objid in parsed_data.iterkeys():
                db_objid = objid
                for user in parsed_data[objid].iterkeys():
                    if user == "*":
                        db_other_permissions = json.dumps(parsed_data[objid][user])
                    else:
                        db_user = user
                        db_user_permissions = json.dumps(parsed_data[objid][user])

            # Validation by user session
            if str(s['id']) == db_user:
                try:
                    #AuthPermission.objects.filter(objid=db_objid).update(objid=db_objid,user=db_user, user_permissions=db_user_permissions, other_permissions=db_other_permissions)
                    tmp = AuthPermission.objects.get(objid=db_objid)
                    tmp.user = db_user
                    tmp.user_permissions = db_user_permissions
                    tmp.other_permissions = db_other_permissions
                    tmp.save()
                except AuthPermission.DoesNotExist:
                    AuthPermission.objects.create(objid=db_objid, user=db_user, user_permissions=db_user_permissions, other_permissions=db_other_permissions)
                response['code'] = 1
            else:
                response['code'] = 0
                #response['debug'] = str(s['id']) + " != " + db_user

        # Get permissions for object
        elif request.META["REQUEST_METHOD"] == "GET":
            objid = request.GET.get('objid','')
            #userid = request.GET.get('userid','')

            response['code'] = 1
            try:
                #tmp = AuthPermission.objects.get(objid=objid, user=userid)
                tmp = AuthPermission.objects.get(objid=objid)
                uperms = json.loads(tmp.user_permissions)
                operms = json.loads(tmp.other_permissions)                
                response['permissions'] = { tmp.objid: { tmp.user: { "read": uperms["read"], "write": uperms["write"] }, "*": { "read": operms["read"], "write": operms["write"] } } }
            except AuthPermission.DoesNotExist:
                response['code'] = 0

        # Detele permissions for object
        elif request.META["REQUEST_METHOD"] == "DELETE":
            objid = request.GET.get('objid','')
            userid = request.GET.get('userid','')

            # Validation by user session
            if str(s['id']) == userid:
                response['code'] = 1
                try:
                    AuthPermission.objects.filter(objid=objid, user=userid).delete()
                except AuthPermission.DoesNotExist:
                    response['code'] = 0
            else:
                response['code'] = 0

        else:
            response['code'] = 0
    else:
        response['code'] = 0

    return HttpResponse(json.dumps(response) + "\n", content_type="application/json")
  
@HttpOptionsDecorator
@VoolksAPIAuthRequired
def delete(request):
    ''' Delete user '''

    response = {}

    (app, key) = get_api_credentials(request)

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

        # Delete user

        # User.objects.filter(email=username, username=username, password=password).delete()
        # NOT WORKING => AUTHENTICATE

        user = authenticate(username=app + "-" + key + "-" + username, password=password)

        if user is not None:
        
            try:
                User.objects.filter(username=app + "-" + key + "-" + username).delete()
            except User.DoesNotExist:
                response['code'] = 57
                response['text'] = "Can't delete user"
                return HttpResponse(json.dumps(response) + "\n", content_type="application/json")

            # Build response

            response['code'] = 1
            response['text'] = "User deleted"
            return HttpResponse(json.dumps(response) + "\n", content_type="application/json")

        else:

            # Can't authenticate

            response['code'] = 46
            response['text'] = "Invalid username or password"
            return HttpResponse(json.dumps(response) + "\n", content_type="application/json")

@HttpOptionsDecorator
@VoolksAPIAuthRequired
def group(request, groupobjid = ""):
    ''' Create group '''
    
    response = {}
    
    (app, key) = get_api_credentials(request)

    session_id = request.META.get('HTTP_X_VOOLKS_SESSION_ID')
    request_content_type_json = request.META.get('CONTENT_TYPE') == "application/json; charset=UTF-8"
    s = SessionStore(session_key=session_id)
    
    if request.META["REQUEST_METHOD"] == "POST" or request.META["REQUEST_METHOD"] == "PUT":
        # Check for valid session
        if 'id' in s:
            # Create group with permissions
            data = []
            if request.META["REQUEST_METHOD"] == "POST":
                if request_content_type_json:
                    decode = urllib.unquote(request.body)
                    decode = decode.replace("[","|")
                    decode = decode.replace("]","|")
                    decode = decode.replace("=","|")
                    sp = decode.split('&')
                    sp0 = sp[0].split('|')
                    sp1 = sp[1].split('|')    
                    data = '{'
                    data = data + '"' + sp0[0] + '":"' + sp0[1] + '",'
                    data = data + '"' + sp1[0] + '":{' + '"' + sp1[1] + '":{' '"' + sp1[3] + '":' + '"' + sp1[5] + '"' + '}' + '}'
                    data = data + '}' 
                else:
                    data = request.POST.items()[0][0]
                    
                parsed_data = json.loads(data)
                groupname = parsed_data["name"]  
                permissions = parsed_data["permissions"]                     
            
                # Error codes if missing data
            
                if groupname == '':
                  response['code'] = 52
                  response['text'] = "Group name not provided"
                  return HttpResponse(json.dumps(response) + "\n", content_type="application/json")
                
                # Create group
                
                db_objid = ""
                try:
                    objgroup = Group.objects.create(name=groupname)
                    
                    db_objid = str(objgroup.id)
                    db_user = str(s['id'])
                    db_user_permissions = json.dumps(permissions)
                    db_other_permissions = ""
                    AuthPermission.objects.create(objid=db_objid, user=db_user, user_permissions=db_user_permissions, other_permissions=db_other_permissions)
                except:
                    # Can't create group
                    
                    response['code'] = 53
                    response['text'] = "Can't create group"
                    return HttpResponse(json.dumps(response) + "\n", content_type="application/json")
                    
                # Build response
                
                response['id'] = db_objid
                return HttpResponse(json.dumps(response) + "\n", content_type="application/json")
                
            if request.META["REQUEST_METHOD"] == "PUT":
                # data = data = request.read()
                data = request.body
                parsed_data = json.loads(data)

                # Error codes if missing data
            
                if groupobjid == '':
                  response['code'] = 56
                  response['text'] = "Group id not provided"
                  return HttpResponse(json.dumps(response) + "\n", content_type="application/json")

                objgroup = Group.objects.get(id=groupobjid)
                users = parsed_data['users']

                try:
                    for db_user in users:
                        objdb_user = User.objects.get(username=app + "-" + key + "-" + db_user)
                        objdb_user.groups.add(objgroup)
                except:
                    # Can't add users to a group
                    
                    response['code'] = 57
                    response['text'] = "Can't add users to a group"
                    return HttpResponse(json.dumps(response) + "\n", content_type="application/json")
                    
                # Build response

                response['code'] = 1
                response['text'] = "Users add to a group"
                return HttpResponse(json.dumps(response) + "\n", content_type="application/json")    
                
        else:
            # Invalid Session      

            response['code'] = 57
            response['text'] = "Invalid Session"   
            return HttpResponse(json.dumps(response) + "\n", content_type="application/json")
            
    if request.META["REQUEST_METHOD"] == "DELETE":
        groupname = request.GET.get('name','')
        
        # Error codes if missing data
        
        if groupname == '':
            response['code'] = 52
            response['text'] = "Group name not provided"
            return HttpResponse(json.dumps(response) + "\n", content_type="application/json")
       
        # Delete group with permissions
       
        try:
            # Group.objects.filter(name=groupname).delete()
            objgroup = Group.objects.get(name=groupname)
            db_objid = objgroup.id
            AuthPermission.objects.filter(objid=db_objid).delete()
            Group.objects.filter(id=db_objid).delete()
            # objgroup.delete()
        except:
            # Can't delete group
            
            response['code'] = 57
            response['text'] = "Can't delete group"
            return HttpResponse(json.dumps(response) + "\n", content_type="application/json")

        # Build response

        response['code'] = 1
        response['text'] = "Group deleted"
        return HttpResponse(json.dumps(response) + "\n", content_type="application/json")
        
@HttpOptionsDecorator
@VoolksAPIAuthRequired
def reset_password(request):
    ''' Recovery user '''

    response = {}        
    
    (app, key) = get_api_credentials(request)
    
    username = request.GET.get('username','')
    
    # Error codes if missing data

    if username == '':
        response['code'] = 56
        response['text'] = "Username not provided"
        return HttpResponse(json.dumps(response) + "\n", content_type="application/json")
        
    try:
        userExists = User.objects.get(username=app + "-" + key + "-" + username)
    except:
        response['code'] = 57
        response['text'] = "Username not exists"
        return HttpResponse(json.dumps(response) + "\n", content_type="application/json")
    
    # Build response
    
    randompassword = ''.join([random.choice(string.letters + string.digits) for i in range(8)])    
    newpassword = md5.new(str(RESET_SECRET_KEY + randompassword + username)).hexdigest()
    userExists.set_password(newpassword)
    userExists.save()
    
    response['newpassword'] = newpassword
    return HttpResponse(json.dumps(response) + "\n", content_type="application/json") 
    
@HttpOptionsDecorator
@VoolksAPIAuthRequired
def change_password(request):
    ''' Change password user '''

    response = {}        
    
    (app, key) = get_api_credentials(request)
    
    username = request.GET.get('username','')
    password = request.GET.get('password','')
    newpassword = request.GET.get('newpassword','')
    
    # Error codes if missing data

    if username == '':
        response['code'] = 56
        response['text'] = "Username not provided"
        return HttpResponse(json.dumps(response) + "\n", content_type="application/json")

    elif password == '':
        response['code'] = 58
        response['text'] = "Password not provided"
        return HttpResponse(json.dumps(response) + "\n", content_type="application/json")
    
    elif newpassword == '':
        response['code'] = 59
        response['text'] = "New password not provided"
        return HttpResponse(json.dumps(response) + "\n", content_type="application/json")
    
    else:
        
        try:
            userExists = User.objects.get(username=app + "-" + key + "-" + username)
            tmp = authenticate(username=app + "-" + key + "-" + username, password=password)
            if tmp is None:
                response['code'] = 60
                response['text'] = "Invalid password"
                return HttpResponse(json.dumps(response) + "\n", content_type="application/json")
        except:
            response['code'] = 57
            response['text'] = "Username not exists"
            return HttpResponse(json.dumps(response) + "\n", content_type="application/json")
            
        userExists.set_password(newpassword)
        userExists.save()
        
        response['newpassword'] = newpassword
        return HttpResponse(json.dumps(response) + "\n", content_type="application/json") 
        