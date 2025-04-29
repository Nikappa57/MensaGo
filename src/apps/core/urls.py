from django.urls import path

from .view import (accreditation, accreditation_pay, homepage, preferences,
                   profile_home, register, login_view, logout_view)

urlpatterns = [
    path("", homepage, name="home"),
    path("profile/", profile_home, name="profile"),
	path("profile/registration/", register, name="register"),
	path("profile/login/", login_view, name="login"),
	path("profile/logout/", logout_view, name="logout"),
    path("profile/preferences/", preferences, name="preferences"),
    path("profile/accreditation/", accreditation, name="accreditation"),
    path("profile/accreditation/pay/",
         accreditation_pay,
         name="accreditation_pay"),
]
