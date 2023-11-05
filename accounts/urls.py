"""urls conf for the accounts app."""
from django.urls import path, re_path

from . import views

app_name = 'users'

urlpatterns = [
    re_path('api/register-by-access-token/' + r'social/(?P<backend>[^/]+)/$', views.register_by_access_token),
    path('api/authentication-test/', views.authentication_test),
]
