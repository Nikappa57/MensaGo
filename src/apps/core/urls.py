from django.urls import path

from .view import (accreditation, accreditation_pay, homepage, preferences,
                   profile_home)

urlpatterns = [
    path("", homepage, name="home"),
    path("profile/", profile_home, name="profile"),
    path("profile/preferences/", preferences, name="preferences"),
    path("profile/accreditation/", accreditation, name="accreditation"),
    path("profile/accreditation/pay/",
         accreditation_pay,
         name="accreditation_pay"),
]
