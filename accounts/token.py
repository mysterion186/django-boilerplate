"""Generate a one time link."""
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


class CustomPasswordResetTokenGenerator(PasswordResetTokenGenerator):
    """Create a one time link with user's information."""

    def _make_hash_value(self, user, timestamp):
        """Create a token based on the user and the current timestamp.

        Args:
            user (models.Users): the user for whom we generate this token.
            timestamp (int): timestam.

        Returns: 
            Str: the token that will be sent to the user. 
        """
        login_timestamp = '' if user.last_login is None else user.last_login.replace(
            microsecond=0, tzinfo=None)
        return (
            six.text_type(user.pk) + user.password +
            six.text_type(login_timestamp) + six.text_type(timestamp)
        )


password_reset_token = CustomPasswordResetTokenGenerator()
