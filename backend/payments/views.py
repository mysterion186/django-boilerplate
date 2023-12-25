"""Views for payment application."""
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateSubscription(APIView):
    """Handle subscription creation."""
    permission_classes = [AllowAny]

    def post(self, request):
        """Handle post request."""
        data = request.data
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[{
                    'price': data["price_id"],
                    'quantity': data.get("quantity", 1)
                }],
                mode='subscription',
                success_url="http://localhost:3000/payment/success",
                cancel_url="http://localhost:3000/payment/cancel"
            )
            return Response({"url":checkout_session.url}, status=status.HTTP_303_SEE_OTHER)
        except Exception as exc:
            raise exc

class Webhook(APIView):
    """Webhook for handling stripes responses."""
    def post(self, request):
        """Handle post request."""
        if settings.STRIPE_WEBHOOK_SECRET:
            signature = request.META["HTTP_STRIPE_SIGNATURE"]
            try:
                event = stripe.Webhook.construct_event(
                    payload=request.body,
                    sig_header=signature,
                    secret=settings.STRIPE_WEBHOOK_SECRET
                )
                data = event["data"]
            except ValueError as exc:
                raise exc
            except stripe.SignatureVerificationError as exc:
                raise exc
            event_type = event["type"]
        else:
            data = request.data["data"]
            event_type = request.data["type"]

        match event_type:
            case 'invoice.paid':
                print("invoice paid")
            case 'invoice.payment_failed':
                print("invoice failed")
            case 'checkout.session.completed':
                print(f"session completed for {data['object']['customer']}")
            case _:
                print(f"unknown event type {event_type}")
