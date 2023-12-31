"""urls for the payments app."""
from django.urls import path
from . import views

app_name = "payments" # pylint: disable=invalid-name

urlpatterns = [
    path(
        'create-subscription',
        view=views.CreateSubscription.as_view(),
        name="create_subscription"
    ),
    path('webhook/', view=views.Webhook.as_view(), name="webhook"),
]
