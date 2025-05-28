from django.urls import path
from django.contrib.auth import views as auth_views

from .view import (accreditation, accreditation_pay, homepage, preferences,
                   profile_home, register, login_view, logout_view, profile_qrcode)

urlpatterns = [
    path("", homepage, name="home"),
    path("profile/", profile_home, name="profile"),
	path("profile/registration/", register, name="register"),
	path("profile/login/", login_view, name="login"),
	path("profile/logout/", logout_view, name="logout"), 
	path("profile/password_reset/", 
         auth_views.PasswordResetView.as_view(), 
         name="password_reset"),
    path("profile/password_reset/done/", 
         auth_views.PasswordResetDoneView.as_view(), 
         name="password_reset_done"),
    path("profile/reset/<uidb64>/<token>/", 
         auth_views.PasswordResetConfirmView.as_view(), 
         name="password_reset_confirm"),
    path("profile/reset/done/", 
         auth_views.PasswordResetCompleteView.as_view(), 
         name="password_reset_complete"),
	
    path("profile/preferences/", preferences, name="preferences"),
    path("profile/accreditation/", accreditation, name="accreditation"),
    path("profile/accreditation/pay/",
         accreditation_pay,
         name="accreditation_pay"),
    path("profile/qrcode/", profile_qrcode, name="profile_qrcode"),

    # Password reset URLs
   
]
