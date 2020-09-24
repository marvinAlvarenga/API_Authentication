from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import AuthSerializer
from .services import AuthGoogleService


class AuthAPIView(APIView):

    serializer_class = AuthSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response({'errors': serializer.errors}, 400)

        access_token = serializer.data['access_token']

        return AuthGoogleService.authorize_user(access_token)
