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

def sign_embedded_chart_url(url):
    parsed_url = urlparse(url)
    payload_data = {
        'sub': 'mythmon',
        'urn:observablehq:path': parsed_url.path,
        'iat': int(datetime.datetime.now().timestamp()),
        'nbf': int(datetime.datetime.now().timestamp()),
        'exp': int((datetime.datetime.now() + datetime.timedelta(minutes=15)).timestamp()),
    }
    token = jwt.encode(payload_data, settings.EMBED_PRIVATE_KEY, algorithm='EdDSA')
    return f"{url}?token={token}"
