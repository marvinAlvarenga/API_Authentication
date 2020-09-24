from django.utils import timezone
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.exceptions import TokenError

from .models import Token


class CustomTokenRefreshSerializer(TokenRefreshSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh_old = attrs['refresh']
        now = timezone.now()

        try:
            token = Token.objects.get(refresh_token=refresh_old, active=True)
            if token.refresh_token_expires > now:
                token.access_token = data['access']
                token.access_token_expires = now + api_settings.ACCESS_TOKEN_LIFETIME

                refresh_new = data.get('refresh', None)
                if refresh_new:
                    token.refresh_token = refresh_new
                    token.refresh_token_expires = now + api_settings.REFRESH_TOKEN_LIFETIME

                token.save()
            else:
                raise TokenError('Token ya expirado en db')
        except Token.DoesNotExist:
            raise TokenError('No se puede refrescar, ha cerrado sesion')

        return data