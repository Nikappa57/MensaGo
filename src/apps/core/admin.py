from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.urls import path

from .models import CustomUser, EconomicalLevel, University
from .view.qr_scanner import QRScannerView, qr_scan_api

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active', 'credit', 'university', 'economical_level')
    list_filter = ('is_staff', 'is_active', 'university', 'economical_level')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'propic')}),
        ('University info', {'fields': ('university', 'economical_level', 'credit')}),
        ('Mensa info', {'fields': ('suffers_from', 'likes')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'university', 'economical_level', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('qr-scanner/', QRScannerView.as_view(), name='qr_scanner'),
            path('qr-scan-api/', qr_scan_api, name='qr_scan_api'),
        ]
        return custom_urls + urls

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(EconomicalLevel)
admin.site.register(University)
