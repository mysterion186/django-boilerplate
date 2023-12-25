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
        except ValueError:
            print("value error")
            return Response({"error": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
        except stripe.SignatureVerificationError as exc:
            raise exc

        if event['type'] == 'checkout.session.completed':
            session = event['data']["object"]
            print(event, session)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
