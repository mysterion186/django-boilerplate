"""Tests related to the subscription to Stripe.
In this folder, there are only the mocked tests.
"""
import json
from unittest.mock import patch

from django.test import TestCase, override_settings
from django.urls import reverse
from django.conf import settings
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

from accounts import models
from .. import models

@override_settings(DEBUG=True)
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

    def _update_mock(self, filename:str):
        """Retrive the mocked file and update the client_reference_id."""
        with open(
            file=str(settings.BASE_DIR) + f"/payments/tests/mock/{filename}",
            mode='r',
            encoding='utf-8'
        ) as file:
            mock_data = json.load(file)
        # set the client_reference_id to the user_ed
        mock_data["data"]["object"]["client_reference_id"] = self.user_ed.id
        return mock_data

    @patch("payments.views.stripe.Webhook.construct_event")
    def test_subscription_creation_correct_card(self, mocked_construct_event):
        """Check the subscription object creation."""
        mock_data = self._update_mock("stripe_session_completed.json")
        mocked_construct_event.return_value = mock_data

        # check that the stripe customer id is set to none for the user
        self.assertIsNone(self.user_ed.stripe_customer_id)

        # subscription request sent by Stripe
        response = self.client.post(
            reverse("payments:webhook"),
            data=json.dumps({}),
            content_type=self.content_type,
            HTTP_STRIPE_SIGNATURE="stripe_signature"
        )

        # check responses
        self.assertEqual(response.status_code, 200)
        self.user_ed.refresh_from_db()
        self.assertIsNotNone(self.user_ed.stripe_customer_id)

    @patch("payments.views.stripe.Webhook.construct_event")
    def test_subscription_creation_failed(self, mocked_construct_event):
        """Check the failed response for a subscription (not working card)."""
        mock_data = self._update_mock("stripe_session_completed_failed.json")
        mocked_construct_event.return_value = mock_data

        # check that the stripe customer id is set to none for the user
        self.assertIsNone(self.user_ed.stripe_customer_id)

        # subscription request sent by Stripe
        response = self.client.post(
            reverse("payments:webhook"),
            data=json.dumps({}),
            content_type=self.content_type,
            HTTP_STRIPE_SIGNATURE="stripe_signature"
        )

        # check responses
        self.assertEqual(response.status_code, 400)
        self.user_ed.refresh_from_db()
        self.assertIsNone(self.user_ed.stripe_customer_id)
