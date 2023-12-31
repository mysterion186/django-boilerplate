"""Command for retrieving all products that exists in our stripe boutique."""
from typing import Any

from django.conf import settings
from django.core.management import BaseCommand
import stripe

from payments.models import Product

stripe.api_key = settings.STRIPE_SECRET_KEY

def retrieve_all_products():
    """Method for retrieving all product object."""
    try:
        all_products = []
        last_product_id = None

        while True:
            products = stripe.Product.list(limit=100, starting_after=last_product_id)
            if not products.data:
                break

            all_products.extend(products.data)
            last_product_id = products.data[-1].id

        return all_products
    except stripe.error.StripeError as e:
        # Handle error
        print(f"Stripe Error: {e}")

def get_all_stripe_objects(stripe_listable):
    objects = []
    get_more = True
    starting_after = None
    while get_more:
        #stripe.Customer implements ListableAPIResource(APIResource):
        resp = stripe_listable.list(limit=100,starting_after=starting_after)
        objects.extend(resp['data'])
        get_more = resp['has_more']
        if len(resp['data'])>0:
            starting_after = resp['data'][-1]['id']
    return objects

class Command(BaseCommand):
    """Command for retrieving all our products on stripe"""
    help = "Retrive stripe products"

    def handle(self, *args: Any, **options: Any) -> None:
        Product.handle_product()
