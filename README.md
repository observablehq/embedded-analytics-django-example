# Framework Embedded Analytics in Django

This repository is an example of importing a JS module from a [Observable Cloud](https://observablehq.com/documentation/data-apps/) data app using signed URLs and embedding it in a [Django](https://www.djangoproject.com/). The Observable Cloud data app provides charts of the number of medals won by countries in the 2024 Olympic Games, optionally broken down by continent.

## Tour

The repository uses Observable Cloud's *signed URLs* feature, which enables secure embedding for private data apps. In this example the data app is public, for demonstration purposes.

The entry point for embedding is in the `index` function in [`charts/views.py`][views]. It generates a signed URL containg a JWT generated with [`PyJWT`](https://pypi.org/project/PyJWT/). Then it renders a Jinja template including that URL to send to the browser:

[views]: https://github.com/observablehq/embedded-analytics-django-example/blob/main/charts/views.py

```py
def index(request):
    signed_url = sign_embedded_chart_url(f"{project_base_url}/medals-chart.js")
    context = {
        'medal_chart_url': signed_url,
    }
    return render(request, "charts/index.html", context)

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
```

The Jinja template at [`charts/templates/charts/index.html`][template] includes a JS script that imports the module from the signed URL, and then renders it into the page:

[template]: https://github.com/observablehq/embedded-analytics-django-example/blob/main/charts/templates/charts/index.html

```jinja
{% extends "./layout.html" %}

{% block content %}
  <h1>Olympic Medals</h1>
  <div id="medals-chart"></div>

  <script type="module">
    const {MedalsChart} = await import("{{ medal_chart_url }}");
    const target = document.querySelector("#medals-chart");
    target.append(await MedalsChart());
  </script>
{% endblock %}
```

## Development

Create and activate virtual environment

```sh
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies

```sh
pip install -r requirements.txt
```

Run the server

```sh
python manage.py runserver
```
