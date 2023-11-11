"""Serializer related to the user"""
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from . import models

class CreateBasicUserSerializer(serializers.ModelSerializer):
    """Handle the creation of a user."""
    password = serializers.CharField(write_only=True)
    password1 = serializers.CharField(write_only=True)

    class Meta:
        """Default meta class."""
        model = models.MyUser
        fields = ["email","biography","password","password1"]

    def validate(self, attrs):
        """Validate data regarding the user's informations."""
        password = attrs.get("password")
        password1 = attrs.pop("password1")

        if password != password1:
            raise serializers.ValidationError(
                {"password": "password must match !"}
            )
        return attrs

    def create(self, validated_data):
        """Create a user based on a validated data.

        Args:
            validated_data (dict): contains necessary information for creating the user.
        
        Returns:
            Users: the newly created user.
        
        Raises:
            serializer.ValidationError in the case the both passwords don't match.
        """
        password = validated_data.pop("password")
        validated_data["password"] = make_password(password=password)
        user = models.MyUser.objects.create(**validated_data)
        return user

class UserSerializer(serializers.ModelSerializer):
    """Serializer to display intel about a user."""
    class Meta:
        """Default meta class."""
        model = models.MyUser
        fields = ["email", "biography"]
