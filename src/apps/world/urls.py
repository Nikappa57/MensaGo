from django.urls import path

from .views import save_user_pos

urlpatterns = [
    path('save-user-pos/', save_user_pos, name='save_user_pos'),
]
