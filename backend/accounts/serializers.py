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

class UpdateBasicUserPasswordSerializer(serializers.ModelSerializer):
    """Serializer for updating basic user's password."""
    old_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    password1 = serializers.CharField(write_only=True)
    class Meta:
        """Default meta class."""
        model = models.MyUser
        fields = ["old_password", "password", "password1"]

    def validate(self, attrs):
        """Validate data for processing (correct old password, new passwords matching)."""
        if "old_password" not in attrs:
            raise serializers.ValidationError(
                {"error": "`old_password` field is required !"}
            )

        try:
            if attrs["password"] != attrs["password1"]:
                raise serializers.ValidationError(
                    {"error": "passwords must match !"}
                )
        except KeyError as exc:
            raise serializers.ValidationError(
                {"error": "Both `password` and `password1` are required"}
            ) from exc
        return attrs

    def validate_old_password(self, value):
        """Validate the given old password."""
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                {"error": "Old password is not correct"}
            )
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data["password"])
        instance.save()
        return {'success': 'password changed'}

class ResetBasicUserPasswordSerializer(serializers.ModelSerializer):
    """Serializer for resetting the basic user's password."""
    password = serializers.CharField(write_only=True)
    password1 = serializers.CharField(write_only=True)
    class Meta:
        """Default meta class."""
        model = models.MyUser
        fields = ["password", "password1"]

    def validate(self, attrs):
        """Validate data regarding the user's password resetting."""
        password = attrs.get("password")
        password1 = attrs.pop("password1")

        if password != password1:
            raise serializers.ValidationError(
                {"password": "password must match !"}
            )
        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data["password"])
        instance.save()
        return {'success': 'password changed'}

class OptionalUserAttributSerializer(serializers.ModelSerializer):
    """Serializer for setting/updating values on a user that are optional.
    Which means almost all values added to the user model.
    """
    class Meta:
        """Default meta class."""
        model = models.MyUser
        fields = ["biography"]

    def validate(self, attrs):
        if "biography" not in attrs:
            raise serializers.ValidationError(
                {"error": "biography field is required !"}
            )
        return attrs

    def validate_biography(self, value):
        """Method for validating attributs."""
        if value == "" or value is None:
            raise serializers.ValidationError(
                {"error": "biography can't be empty"}
            )
        return value
