"""Model for the payment app."""
from typing import Union, List, Dict
from django.db import models
from django.core.validators import MinValueValidator
import stripe

from accounts.models import MyUser
class Invoice(models.Model):
    """Model for handling invoices."""
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=255)
    stripe_invoice = models.CharField(max_length=255)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return self.user.email + " | " + str(self.date)  # pylint: disable=no-member

class Product(models.Model):
    """Model for all our stripe products."""
    class BillingType(models.IntegerChoices):
        """Class for interget choice on the billing type."""
        ONETIME = 1, "one_time"
        RECURRING = 2, "recurring"

        @classmethod
        def get_values(cls, label: str) -> int:
            """Based on the label returns the correct int value.
            
            Args:
                label (str): the labes we're looking for.
            
            Returns:
                int: the corresponding value. Returns 1 as default.
            """
            for choice, choice_label in cls.choices:
                if choice_label == label:
                    return choice
            print(f"Unknown billing type : {label}")
            return cls.ONETIME

    class BillingInterval(models.IntegerChoices):
        """Different type of billing interval."""
        ONETIME = 1, "one_time"
        MONTH = 2, "month"
        YEAR = 3, "year"

        @classmethod
        def get_values(cls, label: str) -> int:
            """Based on the label returns the correct int value.
            
            Args:
                label (str): the labes we're looking for.
            
            Returns:
                int: the corresponding value. Returns 1 as default.
            """
            for choice, choice_label in cls.choices:
                if choice_label == label:
                    return choice
            print(f"Unknown interval : {label}")
            return cls.ONETIME

    product_id = models.CharField(max_length=255)
    price_id = models.CharField(max_length=255, unique=True)
    product_name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    price = models.FloatField(validators=[MinValueValidator(0.0)])
    billing_type = models.IntegerField(choices=BillingType.choices)
    interval = models.IntegerField(choices=BillingInterval.choices, default=BillingInterval.ONETIME)

    @classmethod
    def _get_all_stripe_objects(
        cls,
        stripe_listable: Union[stripe.Product, stripe.Price]
    ) -> List[Union[stripe.Product, stripe.Price]]:
        """Method for accessing all element that stripe can returns us.
         
        Args:
            stripe_listable (Union[stripe.Product, stripe.Price]): object we want to iterate over.
        
        Returns:
            List[Union[stripe.Product, stripe.Price]]: object that contains all the needed values
        """
        objects = []
        get_more = True
        starting_after = None
        while get_more:
            resp = stripe_listable.list(limit=100,starting_after=starting_after)
            objects.extend(resp['data'])
            get_more = resp['has_more']
            if len(resp['data'])>0:
                starting_after = resp['data'][-1]['id']
        return objects

    @classmethod
    def _format_price(cls, prices: List[stripe.Price]) -> Dict[str, str]:
        """Format prices to keep only needed information.
        
        Args:
            prices (List[stripe.Price]): a stripe.Price list object.

        Returns:
            Dict[str, str]: Dictionary with only needed information
        """
        formatted_dict: Dict[str, str] = {}
        for price in prices:
            formatted_dict[price["id"]] = {
                "product": price["product"],
                "recurring": price["recurring"],
                "type": price["type"],
                "price": price["unit_amount_decimal"]
            }
        return formatted_dict

    @classmethod
    def _format_product(cls, products: List[stripe.Product]) -> Dict[str, str]:
        """Format products to keep only needed information.
        
        Args:
            products (List[stripe.Products]): a stripe.Product list object.

        Returns:
            Dict[str, str]: dictionary with only needed information. The key is the product id.
        """
        formatted_dict: Dict[str, str] = {}
        for product in products:
            formatted_dict[product["id"]] = {
                "name": product["name"],
                "description": product["description"],
                "is_active": product["active"]
            }
        return formatted_dict

    @classmethod
    def handle_product(cls) -> int:
        """Method for creating a product.
        
        Returns:
            int: the number of created products
        """
        products: Dict[str, str] = cls._format_product(
            cls._get_all_stripe_objects(stripe.Product)
        )
        prices: stripe.Price = cls._format_price(
            cls._get_all_stripe_objects(stripe.Price)
        )
        count = 0
        for price_id, price in prices.items():
            product = products[price["product"]]
            recurring = price.get('recurring')
            interval = recurring.get('interval') if recurring else 'one_time'
            price['price'] = float(price['price']) / 100.0
            _, created = cls.objects.update_or_create( # pylint: disable=no-member
                price_id=price_id,
                defaults={
                    "product_id": price['product'],
                    "product_name": product['name'],
                    "description": product['description'],
                    "is_active": product['is_active'],
                    "price": price['price'],
                    "billing_type": cls.BillingType.get_values(price['type']),
                    "interval": cls.BillingInterval.get_values(interval)
                }
            )
            count += 1 if created else 0
        return count
