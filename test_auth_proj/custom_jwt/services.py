from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Token


class CustomJWTService():
    TokenClass = RefreshToken

    @classmethod
    def get_payload_from_user(Cls, user):
        refresh_token, access_token = Cls.generate_tokens_for_user(user=user)

        payload = {
            'access_token': str(access_token),
            'refresh_token': str(refresh_token),
        }

        return payload

    @classmethod
    def generate_tokens_for_user(Cls, user):
        refresh_token = Cls.TokenClass.for_user(user)
        access_token = refresh_token.access_token

        return (refresh_token, access_token)


class CustomJWTPersistentService(CustomJWTService):
    @classmethod
    def generate_tokens_for_user(Cls, user):

        refresh_token, access_token = super().generate_tokens_for_user(user)

        now = timezone.now()
        refresh_token_expires = now + refresh_token.lifetime
        access_token_expires = now + access_token.lifetime

        token = Token.objects.create(
            access_token=access_token,
            access_token_expires=access_token_expires,
            refresh_token=refresh_token,
            refresh_token_expires=refresh_token_expires,
            user=user,
        )

        return (refresh_token, access_token)
