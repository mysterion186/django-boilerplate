"""Views relatated to user's authentication 
either the default user of the 3rd party authenticated user.
"""
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import (
    CreateAPIView,
    UpdateAPIView,
    RetrieveAPIView,
)
from rest_framework.views import APIView
from social_django.utils import psa

from . import serializers, models
from .token import password_reset_token
from .permissions import CustomIsAuthenticated

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
                'access': str(jwt_token)
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

class CustomTokenObtainPairView(TokenObtainPairView):
    """This is a simple override of the TokenObtainPairView.
    
    For making sure that the one time link can be used only once I add the last login time
    to the user object. But simplejwt don't add the last login time. This class will handle it.
    """
    def post(self, request, *args, **kwargs):
        """Generate the token and then update last login time for the user."""
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            user = models.MyUser.objects.get(email=request.data["email"])
            user.last_login = timezone.now()
            user.save()
        return response

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

class DisplayUserInformationView(RetrieveAPIView):
    """This class display information on the user. 
    This is a temporary view just to check that the user is authenticated.
    (for test purposes only)
    """
    serializer_class = serializers.UserSerializer
    permission_classes = [CustomIsAuthenticated]

    def get_object(self):
        return self.request.user

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
            EmailMessage(
                subject="Password reset link",
                from_email=settings.EMAIL_HOST_USER,
                to=(user.email,),
                body=f"click on the following link : localhost:3000/{uidb64}/{token}"
            ).send()
            return Response(
                {
                    "status":"success"
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

class ResetPasswordView(APIView):
    """Actual view for resetting the password.
    We assume that the user got the uidb64 and the token from the previous view.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """Handle the token and uidb64 for resetting password."""
        uidb64 = request.data.get("uidb64", None)
        token = request.data.get("token", None)

        if token is None or uidb64 is None:
            return Response(
                {
                    "error": "`token` and `uidb64` are required field"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        try :
            uid = urlsafe_base64_decode(uidb64).decode('ascii')
            user = models.MyUser.objects.get(email=uid)
        except (TypeError, ValueError, OverflowError, models.MyUser.DoesNotExist):
            user = None
            return Response(
                {
                    "error": "The user is not recognized"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        if user is not None and password_reset_token.check_token(user, token):
            serializer = serializers.ResetBasicUserPasswordSerializer(
                user,
                data=request.data,
                partial=True,
                context={"request": request}
            )
            if serializer.is_valid():
                serializer.update(user, request.data)
                # case everything goes smoothly
                return Response(
                    {
                        "detail": "Password successfully reset"
                    },
                    status=status.HTTP_200_OK
                )
            # case the serializer is not valid
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # case the token is not recognized
        return Response({"error": "The link is not recognized"}, status=status.HTTP_400_BAD_REQUEST)

class OptionalUserAttributView(UpdateAPIView):
    """View for updating/setting the optional values of a user."""
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.OptionalUserAttributSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=request.user, data=request.data)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response({"status": "success"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
