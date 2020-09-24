from rest_framework.views import APIView
from rest_framework.response import Response


class UserView(APIView):

    def get(self, request, *args, **kwargs):
        return Response({'message': 'Hello'})
