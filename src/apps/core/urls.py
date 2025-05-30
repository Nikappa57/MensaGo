from django.urls import path
from django.contrib.auth import views as auth_views

from .view import (homepage,
                   profile_home, register, login_view, logout_view, profile_qrcode,
                   change_password)

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
	
    path("profile/password/change/", change_password, name="password_change"),
    path("profile/qrcode/", profile_qrcode, name="profile_qrcode"),

    # Password reset URLs
   
]
