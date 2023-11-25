"""Test related to user's registration."""
import json

from django.test import TestCase, Client
from django.urls import reverse

from .. import models
from .. import serializers

class CreateAccount(TestCase):
    """Class that do tests about user's account creation.
    In this test, the only user's tested are the basic user (MyUser)
    """

    def setUp(self) -> None:
        self.client = Client()
        self.content_type = "application/json"
        self.user_to_create = {
            "email": "ed@elric.com",
            "password": "azerty123azerty123",
            "password1": "azerty123azerty123",
            "biography": "My name is Ed"
        }

        self.created_user = {
            "email": "al@elric.com",
            "password": "azerty123azerty123",
            "password1": "azerty123azerty123",
            "biography": "My name is Al"
        }
        models.MyUser.objects.create_user(
            email=self.created_user["email"],
            password=self.created_user["password"],
            biography=self.created_user["biography"]
        )

    def test_working_account_creation(self):
        """Create a new account -> suppose to work."""
        response = self.client.post(
            reverse("users:create_basic_user"),
            data=json.dumps(self.user_to_create),
            content_type=self.content_type
        )

        # check user is in the db
        user = models.MyUser.objects.get(email=self.user_to_create["email"])
        serializer = serializers.UserSerializer(user)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, 201)

    def test_working_account_creation_without_biography(self):
        """Try to create an account without giving the biography value."""
        self.user_to_create.pop("biography") # remove the value for biography
        response = self.client.post(
            reverse("users:create_basic_user"),
            data=json.dumps(self.user_to_create),
            content_type=self.content_type
        )

        # check user is in the db
        user = models.MyUser.objects.get(email=self.user_to_create["email"])
        serializer = serializers.UserSerializer(user)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, 201)

    def test_account_creation_with_used_email(self):
        """Try to create an account with already used email."""
        response = self.client.post(
            reverse("users:create_basic_user"),
            data=json.dumps(self.created_user),
            content_type=self.content_type
        )

        # check user is in the db
        queryset = models.MyUser.objects.filter(email=self.user_to_create["email"])

        self.assertEqual(queryset.exists(), False)

        # check that email is in the error response
        self.assertTrue(response.data.get("email") is not None)
        self.assertEqual(
            str(response.data["email"][0]),
            "my user with this email address already exists."
        )
        self.assertEqual(response.status_code, 400)

    def test_account_creation_with_diff_password(self):
        """Create account with different passwords."""
        self.user_to_create["password1"] = "differentpassword"

        response = self.client.post(
            reverse("users:create_basic_user"),
            data=json.dumps(self.user_to_create),
            content_type=self.content_type
        )

        # check user is in the db
        queryset = models.MyUser.objects.filter(email=self.user_to_create["email"])

        self.assertEqual(queryset.exists(), False)
        # check that email is in the error response
        self.assertTrue(response.data.get("password") is not None)
        self.assertEqual(
            str(response.data["password"][0]),
            "password must match !"
        )

        self.assertEqual(response.status_code, 400)

    def test_account_creation_missing_password(self):
        """Create account with mission `password`"""
        self.user_to_create.pop("password")
        response = self.client.post(
            reverse("users:create_basic_user"),
            data=json.dumps(self.user_to_create),
            content_type=self.content_type
        )

        queryset = models.MyUser.objects.filter(email=self.user_to_create["email"])

        self.assertEqual(queryset.exists(), False)
        self.assertTrue(response.data.get("password") is not None)
        self.assertEqual(
            str(response.data["password"][0]),
            "This field is required."
        )
        self.assertEqual(response.status_code, 400)

    def test_account_creation_missing_password1(self):
        """Create account with mission `password1`"""
        self.user_to_create.pop("password1")
        response = self.client.post(
            reverse("users:create_basic_user"),
            data=json.dumps(self.user_to_create),
            content_type=self.content_type
        )

        queryset = models.MyUser.objects.filter(email=self.user_to_create["email"])

        self.assertEqual(queryset.exists(), False)
        self.assertTrue(response.data.get("password1") is not None)
        self.assertEqual(
            str(response.data["password1"][0]),
            "This field is required."
        )
        self.assertEqual(response.status_code, 400)
