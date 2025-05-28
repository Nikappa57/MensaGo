from django.urls import path
from .views import mensa_city, mensa_details, toggle_like_dish

urlpatterns = [
    path("<str:city_name>/", mensa_city, name="mensa_city"),
    path("<str:city_name>/<str:mensa_name>/",
         mensa_details,
         name="mensa_details"),
    path("dish/<str:dish_name>/like/", toggle_like_dish, name="toggle_like_dish"),
]
