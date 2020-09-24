from rest_framework import serializers

from .services import AuthGoogleService


class AuthSerializer(serializers.Serializer):

    access_token = serializers.CharField()
