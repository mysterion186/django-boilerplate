"""Model for the custom user"""

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class MyUserManager(BaseUserManager):
    """Handle user's creation."""
    def create_user(self, email, biography=None, password=None):
        """
        Creates and saves a User with the given email. 
        Leave empty all information that are not found with external providers
        e.g Google, Facebook...
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            biography=biography,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, biography=None, password=None):
        """
        Same function, just create a super user here.
        """
        user = self.create_user(
            email,
            password=password,
            biography=biography,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    """The actual User model.
    All information that can't be get by the social auth provider needs to be able
    left blank/null. Easyest way of handling it.
    To force a user to set those information later, use the session middleware.
    """
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    biography = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    @property
    def is_complete(self):
        """Returns a boolean according to the fact that a user is complete.
        
        Should write a condition to check that all the required field for using the app are set.
        """
        # check that biography is not None
        complete = True # assume that the user is always complete
        if self.biography is None:
            complete = False
        return complete
