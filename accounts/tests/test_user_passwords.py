"""Test related to the user's passwords."""
import json

from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

from .. import models
from ..token import password_reset_token

class TestPasswords(TestCase):
    """Test related to user's passwords, reset/update."""

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

    def test_password_update_ok(self):
        """Try to update user's password."""
        # set the token in the header
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))
        data = {
            "old_password": self.information["password"],
            "password": "br4ndn3wp4ssw0rd",
            "password1": "br4ndn3wp4ssw0rd"
        }

        response = self.client.put(
            reverse("users:update-password"),
            data=json.dumps(data),
            content_type=self.content_type
        )

        user = models.MyUser.objects.get(email=self.user_ed.email)

        self.assertTrue(user.check_password(data["password"])) # check password updates
        self.assertTrue(response.data.get("success") is not None)
        self.assertEqual(response.data["success"], "password changed successfully.")
        self.assertEqual(response.status_code, 200)

    def test_password_update_wrong_old_password(self):
        """Update password with wrong old password."""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))
        data = {
            "old_password": self.information["password"] + "wrong_password",
            "password": "br4ndn3wp4ssw0rd",
            "password1": "br4ndn3wp4ssw0rd"
        }

        response = self.client.put(
            reverse("users:update-password"),
            data=json.dumps(data),
            content_type=self.content_type
        )

        user = models.MyUser.objects.get(email=self.user_ed.email)

        self.assertFalse(user.check_password(data["password"])) # check that password is not updated
        # old password is still correct ?
        self.assertTrue(user.check_password(self.information["password"]))
        self.assertTrue(response.data.get("old_password") is not None)
        self.assertEqual(response.data["old_password"]["error"], "Old password is not correct")
        self.assertEqual(response.status_code, 400)

    def test_password_update_with_diff_password(self):
        """Update the password with 2 differents new passwords.
        In this scenario, the old password is correct."""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))
        data = {
            "old_password": self.information["password"],
            "password": "br4ndn3wp4ssw0rd"  + "different_password",
            "password1": "br4ndn3wp4ssw0rd"
        }

        response = self.client.put(
            reverse("users:update-password"),
            data=json.dumps(data),
            content_type=self.content_type
        )

        user = models.MyUser.objects.get(email=self.user_ed.email)

        self.assertFalse(user.check_password(data["password"])) # check that password is not updated
        self.assertTrue(user.check_password(data["old_password"])) # old password is still correct ?
        self.assertTrue(response.data.get("error") is not None)
        self.assertEqual(response.data["error"][0], "passwords must match !")
        self.assertEqual(response.status_code, 400)

    def test_password_update_missing_old_password(self):
        """Update password without the old_password field"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))
        data = {
            "password": "br4ndn3wp4ssw0rd",
            "password1": "br4ndn3wp4ssw0rd"
        }

        response = self.client.put(
            reverse("users:update-password"),
            data=json.dumps(data),
            content_type=self.content_type
        )

        user = models.MyUser.objects.get(email=self.user_ed.email)

        self.assertFalse(user.check_password(data["password"])) # check that password is not updated
        # old password is still correct ?
        self.assertTrue(user.check_password(self.information["password"]))
        self.assertTrue(response.data.get("old_password") is not None)
        self.assertEqual(response.data["old_password"][0], "This field is required.")
        self.assertEqual(response.status_code, 400)

    def test_password_update_missing_password(self):
        """Update password without the password1 field"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))
        data = {
            "old_password": self.information["password"],
            "password": "br4ndn3wp4ssw0rd"
        }

        response = self.client.put(
            reverse("users:update-password"),
            data=json.dumps(data),
            content_type=self.content_type
        )

        user = models.MyUser.objects.get(email=self.user_ed.email)

        self.assertFalse(user.check_password(data["password"])) # check that password is not updated
        self.assertTrue(user.check_password(data["old_password"])) # old password is still correct ?
        self.assertTrue(response.data.get("password1") is not None)
        self.assertEqual(response.data["password1"][0], "This field is required.")
        self.assertEqual(response.status_code, 400)

    def test_password_update_missing_password1(self):
        """Update password without the password field"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))
        data = {
            "old_password": self.information["password"],
            "password": "br4ndn3wp4ssw0rd"
        }

        response = self.client.put(
            reverse("users:update-password"),
            data=json.dumps(data),
            content_type=self.content_type
        )

        user = models.MyUser.objects.get(email=self.user_ed.email)

        self.assertFalse(user.check_password(data["password"])) # check that password is not updated
        self.assertTrue(user.check_password(data["old_password"])) # old password is still correct ?
        self.assertTrue(response.data.get("password1") is not None)
        self.assertEqual(response.data["password1"][0], "This field is required.")
        self.assertEqual(response.status_code, 400)

    def test_generate_one_time_link_with_existing_account(self):
        """Try to generate a one time link to reset user's password."""
        data = {
            "email": self.user_ed.email
        }

        response = self.client.post(
            reverse("users:password_reset_link"),
            data=json.dumps(data),
            content_type=self.content_type
        )

        self.assertEqual(response.data, {"status":"success"})
        self.assertEqual(response.status_code, 201)

    def test_generate_one_time_link_with_not_existing_account(self):
        """Try to generate a one time link for a user that doesn't exist."""
        data = {
            "email": "doesnotexist" +  self.user_ed.email
        }

        response = self.client.post(
            reverse("users:password_reset_link"),
            data=json.dumps(data),
            content_type=self.content_type
        )

        self.assertEqual(response.data, {"error":"There is no user with this email"})
        self.assertEqual(response.status_code, 404)

    def test_reset_password_ok(self):
        """Make sure that we reset the password."""
        uidb64 = urlsafe_base64_encode(str(self.user_ed.email).encode("utf-8"))
        token = password_reset_token.make_token(self.user_ed)
        data = {
            "uidb64": uidb64,
            "token": token,
            "password": "r3s3tp4ssw0rd",
            "password1": "r3s3tp4ssw0rd",
        }

        response = self.client.post(
            reverse("users:reset_password"),
            data=json.dumps(data),
            content_type=self.content_type
        )

        user = models.MyUser.objects.get(email=self.user_ed.email)

        self.assertTrue(user.check_password(data["password"])) # check that password is updated
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"detail": "Password successfully reset"})

    def test_reset_password_diff_password(self):
        """Try to reset the password with different password."""
        uidb64 = urlsafe_base64_encode(str(self.user_ed.email).encode("utf-8"))
        token = password_reset_token.make_token(self.user_ed)
        data = {
            "uidb64": uidb64,
            "token": token,
            "password": "r3s3tp4ssw0rd",
            "password1": "r3s3tp4ssw0rd" + "differentpassword",
        }

        response = self.client.post(
            reverse("users:reset_password"),
            data=json.dumps(data),
            content_type=self.content_type
        )

        user = models.MyUser.objects.get(email=self.user_ed.email)

        self.assertFalse(user.check_password(data["password"])) # check that password is not updated
        # old password is still correct ?
        self.assertTrue(user.check_password(self.information["password"])) 
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["password"][0], "password must match !")

    def test_one_time_link_works_once_after_reset(self):
        """Make sure that the one time links only works once.
        In this case, check that the link is not active once the user used it.
        """
        uidb64 = urlsafe_base64_encode(str(self.user_ed.email).encode("utf-8"))
        token = password_reset_token.make_token(self.user_ed)
        data = {
            "uidb64": uidb64,
            "token": token,
            "password": "r3s3tp4ssw0rd",
            "password1": "r3s3tp4ssw0rd",
        }

        _ = self.client.post(
            reverse("users:reset_password"),
            data=json.dumps(data),
            content_type=self.content_type
        )

        user = models.MyUser.objects.get(email=self.user_ed.email)

        self.assertTrue(user.check_password(data["password"])) # check that password is updated

        data_after_reset = {
            "uidb64": uidb64,
            "token": token,
            "password": "4ft3rr3s3tp4ssw0rd",
            "password1": "4ft3rr3s3tp4ssw0rd",
        }
        # use the same token/ reset link again
        response_after_reset = self.client.post(
            reverse("users:reset_password"),
            data=json.dumps(data_after_reset),
            content_type=self.content_type
        )

        user = models.MyUser.objects.get(email=self.user_ed.email)

        # check that password is not updated
        self.assertFalse(user.check_password(data_after_reset["password"]))
        # old password is still correct ?
        self.assertTrue(user.check_password(data["password"]))
        self.assertEqual(response_after_reset.status_code, 400)
        self.assertEqual(response_after_reset.data, {"error": "The link is not recognized"})


    def test_one_time_link_after_login(self):
        """Check that if the user logged in after if requested a reset link
        the link does not work (because there is the last_login value inside the link)."""
        # generate to link (token/uidb64)
        uidb64 = urlsafe_base64_encode(str(self.user_ed.email).encode("utf-8"))
        token = password_reset_token.make_token(self.user_ed)

        # make a request to force the last_login time update
        _ = self.client.post(
            reverse("users:token_obtain_pair"),
            data=json.dumps({
                "email": self.information["email"],
                "password": self.information["password"]
            }),
            content_type=self.content_type
        )

        data = {
            "uidb64": uidb64,
            "token": token,
            "password": "r3s3tp4ssw0rd",
            "password1": "r3s3tp4ssw0rd",
        }

        response = self.client.post(
            reverse("users:reset_password"),
            data=json.dumps(data),
            content_type=self.content_type
        )

        user = models.MyUser.objects.get(email=self.user_ed.email)

        # check that password is not updated
        self.assertFalse(user.check_password(data["password"]))
        # old password is still correct ?
        self.assertTrue(user.check_password(self.information["password"])) 
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {"error": "The link is not recognized"})

    def test_reset_password_wrong_uidb64(self):
        """Reset passwords (equals) with wrong uidb64 value."""
        uidb64 = urlsafe_base64_encode(str(self.user_ed.email).encode("utf-8")) + "wrong_uidb64"
        token = password_reset_token.make_token(self.user_ed)
        data = {
            "uidb64": uidb64,
            "token": token,
            "password": "r3s3tp4ssw0rd",
            "password1": "r3s3tp4ssw0rd",
        }

        response = self.client.post(
            reverse("users:reset_password"),
            data=json.dumps(data),
            content_type=self.content_type
        )

        user = models.MyUser.objects.get(email=self.user_ed.email)

        self.assertFalse(user.check_password(data["password"])) # check that password is not updated
        # old password is still correct ?
        self.assertTrue(user.check_password(self.information["password"]))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, {"error": "The user is not recognized"})

    def test_reset_password_wrong_token(self):
        """Reset passwords (equals) with wrong token value."""
        uidb64 = urlsafe_base64_encode(str(self.user_ed.email).encode("utf-8"))
        token = password_reset_token.make_token(self.user_ed) + "wrong_token"
        data = {
            "uidb64": uidb64,
            "token": token,
            "password": "r3s3tp4ssw0rd",
            "password1": "r3s3tp4ssw0rd",
        }

        response = self.client.post(
            reverse("users:reset_password"),
            data=json.dumps(data),
            content_type=self.content_type
        )

        user = models.MyUser.objects.get(email=self.user_ed.email)

        self.assertFalse(user.check_password(data["password"])) # check that password is not updated
        # old password is still correct ?
        self.assertTrue(user.check_password(self.information["password"]))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {"error": "The link is not recognized"})
