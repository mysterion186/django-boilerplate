"""Tests about the users.
Can be login, setting/updating value, checking permissions...
"""
import json

from django.test import TestCase, RequestFactory
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken

from .. import models
from .. import permissions

class TestUser(TestCase):
    """Test related to user's information/permissions."""

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
        # self.user_ed.set_password(self.information["password"])
        self.user_ed.save()

        self.access_token = AccessToken.for_user(self.user_ed)

    def test_login_correct_credentials(self):
        """Login in with correct credentials."""
        data = {
            "email": self.information["email"],
            "password": self.information["password"]
        }

        response = self.client.post(
            reverse("users:token_obtain_pair"),
            data=json.dumps(data),
            content_type=self.content_type
        )

        self.assertTrue(response.data.get("access") is not None)
        self.assertTrue(response.data.get("refresh") is not None)
        self.assertEqual(response.status_code, 200)

    def test_login_wrong_credentials(self):
        """Login witn incorrect crendentials."""
        data = {
            "email": self.information["email"],
            "password": self.information["password"] + "wrong_password"
        }

        response = self.client.post(
            reverse("users:token_obtain_pair"),
            data=json.dumps(data),
            content_type=self.content_type
        )

        self.assertTrue(response.data.get("detail") is not None)
        self.assertEqual(
            response.data,
            {"detail": "No active account found with the given credentials"}
        )
        self.assertEqual(response.status_code, 401)

    def test_custom_is_authenticated_working(self):
        """Test the response for the custom permission.
        This permission, forces to user to set all it's optional attribut.
        """
        request = RequestFactory().get(reverse("users:delete_me_please"))

        request.user = self.user_ed
        permissions_check = permissions.CustomIsAuthenticated()
        permission = permissions_check.has_permission(request, None)

        self.assertTrue(permission)

    def test_custom_is_authenticated_not_working(self):
        """Test the response for the custom permission.
        Check that user with not all optional field set don't work
        """
        request = RequestFactory().get(reverse("users:delete_me_please"))

        user = models.MyUser.objects.create_user(
            email="al@elric.com",
            password="azerty123azerty123"
        )
        request.user = user
        permissions_check = permissions.CustomIsAuthenticated()
        permission = permissions_check.has_permission(request, None)

        self.assertFalse(permission)

    def test_is_authenticated_working(self):
        """Test the response for the IsAuthenticated permission.
        This permission, forces to user to set all it's optional attribut.
        """
        request = RequestFactory().get(reverse("users:delete_me_please"))

        request.user = self.user_ed
        permissions_check = IsAuthenticated()
        permission = permissions_check.has_permission(request, None)

        self.assertTrue(permission)

    def test_is_authenticated_not_working(self):
        """Test the response for the IsAuthenticated permission.
        Check that user with not all optional field set don't work
        """
        request = RequestFactory().get(reverse("users:delete_me_please"))

        user = models.MyUser.objects.create_user(
            email="al@elric.com",
            password="azerty123azerty123"
        )
        request.user = user
        permissions_check = IsAuthenticated()
        permission = permissions_check.has_permission(request, None)

        self.assertTrue(permission)

    def test_set_first_time_optional_attribut(self):
        """Test the setting (first time) of optional settings.
        This is a user that does not have a biography in first place.
        """
        user = models.MyUser.objects.create_user(
            email="al@elric.com",
            password="azerty123azerty123"
        )

        access_token = AccessToken.for_user(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(access_token))

        data = {
            "biography": "My name is Al"
        }

        response = self.client.put(
            reverse("users:set_optional_field"),
            data=json.dumps(data),
            content_type=self.content_type
        )

        user.refresh_from_db()
        self.assertEqual(user.biography, data["biography"])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"status": "success"})

    def test_update_optional_attribut(self):
        """Test for updating an existing optional attribut."""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))

        data = {
            "biography": "New biography for testing"
        }

        response = self.client.put(
            reverse("users:set_optional_field"),
            data=json.dumps(data),
            content_type=self.content_type
        )

        self.user_ed.refresh_from_db()
        self.assertEqual(self.user_ed.biography, data["biography"])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"status": "success"})

    def test_update_optional_attribut_empty_value(self):
        """Test for updating an existing optional attribut."""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))

        data = {
            "biography": ""
        }

        response = self.client.put(
            reverse("users:set_optional_field"),
            data=json.dumps(data),
            content_type=self.content_type
        )

        self.assertTrue(response.data.get("biography") is not None)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data["biography"],
            {"error": "biography can't be empty"}
        )

    def test_update_optional_attribut_without_value(self):
        """Test for updating an existing optional attribut."""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))

        data = {
            "unwanted_value": ""
        }

        response = self.client.put(
            reverse("users:set_optional_field"),
            data=json.dumps(data),
            content_type=self.content_type
        )

        self.assertTrue(response.data.get("error") is not None)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data["error"][0],
            "biography field is required !"
        )

    def test_update_optional_attribut_no_authentication(self):
        """Test for updating an existing optional attribut."""

        data = {
            "biography": "New biography for testing"
        }

        response = self.client.put(
            reverse("users:set_optional_field"),
            data=json.dumps(data),
            content_type=self.content_type
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, {"detail": "Authentication credentials were not provided."})
