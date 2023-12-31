"""Command for retrieving all products that exists in our stripe boutique."""
from typing import Any

from django.conf import settings
from django.core.management import BaseCommand
import stripe

from payments.models import Product

stripe.api_key = settings.STRIPE_SECRET_KEY

class Command(BaseCommand):
    """Command for retrieving all our products on stripe"""
    help = "Retrive stripe products"

    def handle(self, *args: Any, **options: Any) -> None:
        count: int = Product.handle_product()
        print(f"{count} new product where created")
