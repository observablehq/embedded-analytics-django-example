from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', include("charts.urls")),
    path('admin/', admin.site.urls),
    *staticfiles_urlpatterns(),
]
