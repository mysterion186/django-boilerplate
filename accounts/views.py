"""Views relatated to user's authentication 
either the default user of the 3rd party authenticated user.
"""
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import (
    CreateAPIView,
    UpdateAPIView,
)
from rest_framework.views import APIView
from social_django.utils import psa

from . import serializers, models
from .token import password_reset_token

@api_view(['POST'])
@permission_classes([AllowAny])
@psa()
def register_by_access_token(request, backend):
    """Take the accessToken given by the 3rd party authentication provider
    in order to authenticate the user (create the account if the user does not exist).
    Once the user is authenticated (or created) he will receive a JWT token 
    for authanticating himself in oup app.
    """
    token = request.data.get('access_token')
    user = request.backend.do_auth(token)
    if user:
        jwt_token = AccessToken.for_user(user=user)
        return Response(
            {
                'jwt_token': str(jwt_token)
            },
            status=status.HTTP_200_OK,
            )
    return Response(
        {
            'errors': {
                'token': 'Invalid token'
                }
        },
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(['GET', 'POST'])
def authentication_test(request):
    """Basic endpoint for testing purpose only."""
    print(request.user)
    return Response(
        {
            'message': "User successfully authenticated"
        },
        status=status.HTTP_200_OK,
    )

class CreateBasicUserView(CreateAPIView):
    """View for creating basic user."""
    serializer_class = serializers.CreateBasicUserSerializer
    permission_classes = [AllowAny]

class UpdateBasicUserPasswordView(UpdateAPIView):
    """View for allowing the basic user to update it's password."""
    serializer_class = serializers.UpdateBasicUserPasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        """Override the update method in order to include a custom success message."""
        serializer = self.get_serializer(instance=request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        response_data = {
            "success": "password changed successfully."
        }
        return Response(response_data, status=status.HTTP_200_OK)

class SendResetOneTimeLinkView(APIView):
    """Generate a one time link for the user.
    We'll use it for confirm his will to reset it's password."""
    permission_classes = [AllowAny]

    def post(self, request):
        """User send his email. We'll send the link via email."""
        try:
            user = models.MyUser.objects.get(email=request.data["email"])
            token = password_reset_token.make_token(user)
            uidb64 = urlsafe_base64_encode(str(user.email).encode('utf-8'))
            return Response(
                {
                    "status":"success",
                    "token": token,
                    "uidb64": uidb64
                },
                status=status.HTTP_201_CREATED
            )
        except KeyError:
            return Response({"error": "`email` is required"}, status=status.HTTP_400_BAD_REQUEST)
        except models.MyUser.DoesNotExist:
            return Response(
                {
                    "error": "There is no user with this email"
                },
                status=status.HTTP_404_NOT_FOUND
            )
