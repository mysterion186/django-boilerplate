"""Views relatated to user's authentication 
either the default user of the 3rd party authenticated user.
"""
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from social_django.utils import psa

from . import serializers

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
