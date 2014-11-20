import requests
from decorators import HttpOptionsDecorator, VoolksAPIAuthRequired
from django.http import HttpResponse, HttpResponseRedirect
import json
from django.core.mail import EmailMultiAlternatives
from datetime import datetime
from django.contrib.sessions.backends.db import SessionStore

USER_SESSION_URL = "http://localhost:8000/"
DATABASE_NAME = "test"
MAIL_SEND_LIMIT_COUNT = 10
MAIL_SEND_LIMIT_TIME = 60 * 5

def get_api_credentials(request):
    ''' Get app id and api key '''

    app = request.META.get('HTTP_X_VOOLKS_APP_ID')
    key = request.META.get('HTTP_X_VOOLKS_API_KEY')
    
    return (app, key)

@HttpOptionsDecorator
@VoolksAPIAuthRequired
def sendmail(request):

    sessionid = request.META.get('HTTP_X_VOOLKS_SESSION_ID')
    (app, key) = get_api_credentials(request)
    try:
        request_content_type_json = request.META["CONTENT_TYPE"] == "application/json; charset=UTF-8"
    except:
        request_content_type_json = False
    
    if request.method == "POST":
        if not sessionid:
            return HttpResponse(json.dumps({"error":"Invalid session (empty)","code":"53"}) + "\n", content_type="application/json")
        else:
            session = validate_session(sessionid, app, key)
            if not "userid" in session:
                return HttpResponse(json.dumps({"error":"Invalid session","code":"54"}) + "\n", content_type="application/json")
            else:
                if request_content_type_json:
                    data = "{"
                    params = dict([p.split('=') for p in request.body.split('&')])
                    for key2 in params: 
                        data = data + '"' + key2 + '":"' +params[key2] + '",'
                    data = data + "}"
                    data = data.replace(",}","}")
                else:
                    data = request.POST.items()[0][0]
                parsed_data = json.loads(data)

                now = datetime.now()
                totalsecondsNow = int (now.strftime("%s")) 
                try:
                    s = SessionStore(session_key=sessionid)
                    if 'mail_send_limit_count' in s:
                        if totalsecondsNow - s['mail_send_limit_time'] <= MAIL_SEND_LIMIT_TIME and  s['mail_send_limit_count'] >= MAIL_SEND_LIMIT_COUNT:
                            return HttpResponse(json.dumps({"error":"Error limit sending mail","code":"55"}) + "\n", content_type="application/json")
                        else:
                            s['mail_send_limit_count'] = s['mail_send_limit_count'] + 1
                            s['mail_send_limit_time'] = totalsecondsNow
                            s.save()
                    else:
                        s['mail_send_limit_count'] = 1
                        s['mail_send_limit_time'] = totalsecondsNow
                        s.save()
                    
                    msg = EmailMultiAlternatives(parsed_data["subject"], parsed_data["html"], parsed_data["from"], [parsed_data["to"]])
                    msg.attach_alternative(parsed_data["html"], "text/html")
                    result = msg.send()	
                                        
                    response = { 'sent': result }
                    return HttpResponse(json.dumps(response) + "\n", content_type="application/json");
                    
                except:
                    return HttpResponse(json.dumps({"error":"Error sending mail","code":"500"}) + "\n", content_type="application/json")    
    else:
        return HttpResponse(json.dumps({"error":"Invalid method","code":"405"}) + "\n", content_type="application/json")

def validate_session(sessionid, app, key):
    ''' Check if user session is valid using an external API (auth.api)'''

    import requests
    res = requests.get(USER_SESSION_URL + 'validate/' + sessionid + '/', headers={'X-Voolks-App-Id': app, 'X-Voolks-Api-Key': key},verify=False)    
    response = json.loads(res.text)
    return response                