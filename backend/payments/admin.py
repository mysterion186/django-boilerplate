"""Admin for payment app."""
from django.contrib import admin
from . import models

admin.site.register(models.Invoice)
admin.site.register(models.Product)
