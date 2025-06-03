from django.urls import path

from .views import get_mensa_data
from django.urls import re_path

urlpatterns = [
    re_path(r'^(?P<name>.+)/$', get_mensa_data, name="get_mensa_data")
]
