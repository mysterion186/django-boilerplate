"""Model for the payment app."""
from django.db import models

from accounts.models import MyUser
class Invoice(models.Model):
    """Model for handling invoices."""
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=255)
    stripe_id = models.CharField(max_length=255)
    stripe_invoice = models.CharField(max_length=255)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return self.user.email + " | " + str(self.date)  # pylint: disable=no-member
