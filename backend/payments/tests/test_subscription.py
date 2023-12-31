"""Tests related to the subscription to Stripe.
In this folder, there are only the mocked tests.
"""
import json

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

from accounts import models
from .. import models

class TestSubscription(TestCase):
    """Test related to subscription."""

    def setUp(self) -> None:
        self.client = APIClient()
        self.content_type = "application/json"
        self.information = {
            "email": "ed@elric.com",
            "password": "azerty123azerty123",
            "password1": "azerty123azerty123",
            "biography": "My name is Ed"
        }
        self.user_ed = models.MyUser.objects.create_user(
            email=self.information["email"],
            biography=self.information["biography"],
            password=self.information["password"]
        )
        self.user_ed.save()
        self.access_token = AccessToken.for_user(self.user_ed)

    def test_subscription_creation(self):
        """Check the subscription object creation."""
