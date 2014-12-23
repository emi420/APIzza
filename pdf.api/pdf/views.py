import requests
from decorators import HttpOptionsDecorator, VoolksAPIAuthRequired
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.template.loader import render_to_string
from django_xhtml2pdf.utils import generate_pdf
from pdf import settings
from os import urandom
import json
import StringIO
import ho.pisa as pisa
import re

@HttpOptionsDecorator
@VoolksAPIAuthRequired
def xhtml2pdf(request):

    url = ""
    htmlsrc = ""
    
    if request.META["REQUEST_METHOD"] == "POST":
        htmlsrc = request.POST.items()[0][0]
    else:
        url = request.GET['url']
        r = requests.get(url, verify=False)
        htmlsrc = r.text

    html_urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+/', htmlsrc)
    for html_url in html_urls:
        if html_url.find(".voolks.com/") < 0 and html_url.find("/voolks.com/") < 0:
            return HttpResponse(json.dumps({"error":"External URL not permitted: " + html_url,"code":"2"}) + "\n", content_type="application/json")

    html = render_to_string('blank.html', {'html': htmlsrc},
                            context_instance=RequestContext(request))

    if request.META["REQUEST_METHOD"] == "POST":
        rhash = str(urandom(16).encode('hex'))
        filename = rhash + ".pdf"
        result = open(settings.MEDIA_ROOT + filename, 'wb') 
        pdf = pisa.pisaDocument(
                StringIO.StringIO(html.encode('ascii', 'xmlcharrefreplace')), result)
        result.close()
        url = "/media/" + filename
        return HttpResponse(json.dumps({'id': rhash, 'url': url}), content_type="application/json"); 
    else:
        result = StringIO.StringIO()
        pdf = pisa.pisaDocument(
                StringIO.StringIO(html.encode('ascii', 'xmlcharrefreplace')),
                result, link_callback=link_callback)
        return HttpResponse(result.getvalue(), mimetype='application/pdf')


def link_callback(uri, rel):
    if uri.find('http') != -1:
        return uri
    return os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
