from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("afr", views.continent("Africa", "AFR"), name="continent-afr"),
    path("ame", views.continent("Americas", "AME"), name="continent-ame"),
    path("asi", views.continent("Asia", "ASI"), name="continent-asi"),
    path("eur", views.continent("Europe", "EUR"), name="continent-eur"),
    path("oce", views.continent("Oceania", "OCE"), name="continent-oce"),
]
