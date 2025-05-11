from django.urls import path
from .views import mensa_city, mensa_details

urlpatterns = [
    path("<str:city_name>/", mensa_city, name="mensa_city"),
    path("<str:city_name>/<str:mensa_name>/",
         mensa_details,
         name="mensa_details"),
]
