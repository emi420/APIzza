import requests
from decorators import HttpOptionsDecorator, VoolksAPIAuthRequired
from django.http import HttpResponse, HttpResponseRedirect
import json
from django.core.mail import EmailMultiAlternatives

@HttpOptionsDecorator
@VoolksAPIAuthRequired
def sendmail(request):

    if request.method == "POST":

        try:

            data = request.POST.items()[0][0]

            parsed_data = json.loads(data)

            msg = EmailMultiAlternatives(parsed_data["subject"], parsed_data["html"], parsed_data["from"], [parsed_data["to"]])
            msg.attach_alternative(parsed_data["html"], "text/html")
            result = msg.send()	

            response = { 'sent': result }

            return HttpResponse(json.dumps(response) + "\n", content_type="application/json");

        except:
            return HttpResponse(json.dumps({"error":"Error sending mail","code":"500"}) + "\n", content_type="application/json")

    else:
        return HttpResponse(json.dumps({"error":"Invalid method","code":"405"}) + "\n", content_type="application/json")