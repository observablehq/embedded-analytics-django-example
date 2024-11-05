from urllib.parse import urlparse
import datetime

import jwt
from django.shortcuts import render
from django.conf import settings

def index(request):
    signed_url = sign_embedded_chart_url("https://observablehq.observablehq.cloud/olympian-embeds/medals-chart.js")
    context = {
        'medal_chart_url': signed_url,
    }
    return render(request, "charts/index.html", context)

def continent(name, code):
    def fn(request):
        signed_url = sign_embedded_chart_url(f"https://observablehq.observablehq.cloud/olympian-embeds/continent/{code}/chart.js")
        context = {
            'medal_chart_url': signed_url,
            'continent_name': name,
            'continent_code': code,
        }
        return render(request, "charts/continent.html", context)
    return fn

SIGNATURE_ALIGN_MIN = 5
SIGNATURE_VALIDITY_MIN = SIGNATURE_ALIGN_MIN * 2

def sign_embedded_chart_url(url):
    parsed_url = urlparse(url)

    nbf = datetime.datetime.now().timestamp()
    nbf -= (nbf % (SIGNATURE_ALIGN_MIN * 60))
    exp = nbf + (SIGNATURE_VALIDITY_MIN * 60)

    payload_data = {
        'sub': 'django-example',
        'urn:observablehq:path': parsed_url.path,
        'nbf': int(nbf),
        'exp': int(exp),
    }
    token = jwt.encode(payload_data, settings.EMBED_PRIVATE_KEY, algorithm='EdDSA')
    return f"{url}?token={token}"
