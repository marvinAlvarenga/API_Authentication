from django.utils import timezone
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import  InvalidToken
from rest_framework.exceptions import AuthenticationFailed

from .models import Token


class CustomJWTAuthentication(JWTAuthentication):

    def authenticate(self, request):
        try:
            original_result_tuple = super().authenticate(request)

            if original_result_tuple is not None:

                user = original_result_tuple[0]
                raw_token = str(original_result_tuple[1])

                token = Token.objects.get(access_token=raw_token, active=True)

                if timezone.now() > token.access_token_expires:
                    raise AuthenticationFailed('Session caducada por el admin')

        except InvalidToken:
            raise AuthenticationFailed('Error con el token o ha expirado')

        except Token.DoesNotExist:
            raise AuthenticationFailed('Session caducada')

        return original_result_tuple
