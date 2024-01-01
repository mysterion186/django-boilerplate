"""Views for payment application."""
from typing import Optional, Dict
import logging

from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
import stripe

from payments.models import Invoice
from accounts.models import MyUser

logger = logging.getLogger("project")
stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateSubscription(APIView):
    """Handle subscription creation."""

    def post(self, request):
        """Handle post request."""
        data = request.data
        stripe_customer_id: Optional[str] = request.user.stripe_customer_id
        try:
            sessions_params: Dict = {
                "client_reference_id": request.user.id,
                "line_items": [{
                    'price': data["price_id"],
                    'quantity': data.get("quantity", 1)
                }],
                "mode": 'subscription',
                "success_url": "http://localhost:3000/payment/success",
                "cancel_url": "http://localhost:3000/payment/cancel"
            }
            if stripe_customer_id:
                sessions_params["customer"] = stripe_customer_id
            checkout_session = stripe.checkout.Session.create(
                **sessions_params
            )
            return Response({"url":checkout_session.url}, status=status.HTTP_303_SEE_OTHER)
        except Exception as exc: # pylint: disable=broad-exception-caught
            logger.error("Something went wrong with subscription creation %s", str(exc))
            return Response({"error": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST)

class Webhook(APIView):
    """Webhook for handling stripes responses."""
    permission_classes = [AllowAny]

    def post(self, request):
        """Handle post request."""
        payload = request.body
        sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except ValueError as exc:
            logger.error("There is a value error when listening on the webhook %s", exc)
            return Response({"error": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
        except stripe.SignatureVerificationError as exc:
            logger.error("Problem with the signature verification %s", exc)
            return Response(
                {"error": "There is an issue with the signature verification"},
                status=status.HTTP_400_BAD_REQUEST
            )

        logger.info("Event type %s", event["type"])
        logger.info("Event object %s", event)
        if event['type'] == 'checkout.session.completed':
            session = event['data']["object"]
            user_id = session.get("client_reference_id")
            stripe_id = session.get("id")
            stripe_customer_id = session.get("customer")
            stripe_invoice = session.get("invoice")

            user = MyUser.objects.get(pk=user_id)
            user.stripe_customer_id = stripe_customer_id
            user.save()

            invoice = Invoice(
                user=user,
                stripe_invoice=stripe_invoice,
                stripe_id=stripe_id
            )
            invoice.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
