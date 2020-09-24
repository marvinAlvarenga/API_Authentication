from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenRefreshView

from .models import Token
from .serializers import CustomTokenRefreshSerializer


class LogOutAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        raw_token = str(request.auth)

        token = Token.objects.get(access_token=raw_token)
        token.active = False
        token.save()

        return Response({'message': 'Cerro sesion'})


class TokenRefreshAPIView(TokenRefreshView):

    serializer_class = CustomTokenRefreshSerializer
