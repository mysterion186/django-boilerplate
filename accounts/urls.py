"""urls conf for the accounts app."""
from django.urls import path, re_path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

app_name = 'users'

urlpatterns = [
    # social provider related endpoints
    re_path(
        'register-by-access-token/' + r'social/(?P<backend>[^/]+)/$',
        views.register_by_access_token
    ),
    path('authentication-test/', views.authentication_test),

    # all users related endpoint
    path('token', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),

    # basic user related endpoint
    path('create-user', view=views.CreateBasicUserView.as_view(), name='create_basic_user'),
    path(
        'update-password',
        view=views.UpdateBasicUserPasswordView.as_view(),
        name='update-password'
    ),
    path(
        'password-reset-link',
        view=views.SendResetOneTimeLinkView.as_view(),
        name="password_reset_link"
    ),
]
