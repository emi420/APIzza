import requests
from decorators import HttpOptionsDecorator, VoolksAPIAuthRequired
from django.http import HttpResponse, HttpResponseRedirect
import json
from django.core.mail import EmailMultiAlternatives

@HttpOptionsDecorator
@VoolksAPIAuthRequired
def sendmail(request):

    request_content_type_json = request.META["CONTENT_TYPE"] == "application/json; charset=UTF-8"
    if request.method == "POST":

         if request_content_type_json:
            data = "{"
            params = dict([p.split('=') for p in request.body.split('&')])
            for key in params: 
                data = data + '"' + key + '":"' +params[key] + '",'
            data = data + "}"
            data = data.replace(",}","}")
        else:
            data = request.POST.items()[0][0]
            parsed_data = json.loads(data)

        try:

            msg = EmailMultiAlternatives(parsed_data["subject"], parsed_data["html"], parsed_data["from"], [parsed_data["to"]])
            msg.attach_alternative(parsed_data["html"], "text/html")
            result = msg.send()	

            response = { 'sent': result }

            return HttpResponse(json.dumps(response) + "\n", content_type="application/json");

        except:
            return HttpResponse(json.dumps({"error":"Error sending mail","code":"500"}) + "\n", content_type="application/json")

    else:
        return HttpResponse(json.dumps({"error":"Invalid method","code":"405"}) + "\n", content_type="application/json")
