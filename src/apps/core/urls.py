from django.urls import path
from django.contrib.auth import views as auth_views

from .view import (homepage,
                   profile_home, register, login_view, logout_view, profile_qrcode,
                   change_password, terms_of_service, privacy_policy)
from .view.qr_scanner import QRScannerView, qr_scan_api
from .forms import CustomPasswordResetForm, CustomSetPasswordForm

urlpatterns = [
    path("", homepage, name="home"),
    path("profile/", profile_home, name="profile"),
	path("profile/registration/", register, name="register"),
	path("profile/login/", login_view, name="login"),
	path("profile/logout/", logout_view, name="logout"), 
	path("profile/password_reset/", 
         auth_views.PasswordResetView.as_view(
			form_class=CustomPasswordResetForm),
        	 name="password_reset"),
    path("profile/password_reset/done/", 
         auth_views.PasswordResetDoneView.as_view(), 
         name="password_reset_done"),
    path("profile/reset/<uidb64>/<token>/", 
         auth_views.PasswordResetConfirmView.as_view(
			form_class=CustomSetPasswordForm
		 ), 
         name="password_reset_confirm"),
    path("profile/reset/done/", 
         auth_views.PasswordResetCompleteView.as_view(), 
         name="password_reset_complete"),
	
    path("profile/password/change/", change_password, name="password_change"),
    path("profile/qrcode/", profile_qrcode, name="profile_qrcode"),
    path("terms-of-service/", terms_of_service, name="terms_of_service"),
    path("privacy-policy/", privacy_policy, name="privacy_policy"),

    # Password reset URLs
    
    # QR Scanner API
    path("admin-qr-scan-api/", qr_scan_api, name="admin_qr_scan_api"),
]
