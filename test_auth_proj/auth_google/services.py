from pydoc import locate

import requests
from requests.exceptions import ConnectionError
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_jwt.settings import api_settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from test_auth_proj.custom_jwt.services import CustomJWTService, CustomJWTPersistentService
from .errors import ThirdPartyServiceError


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class AuthGoogleService():

    JWTService = CustomJWTPersistentService
    ContractClass = locate(settings.AUTH_INTEGRATION['CONTRACT'])
    ServiceClass = locate(settings.AUTH_INTEGRATION['SERVICE'])

    @classmethod
    def authorize_user(Cls, access_token):
        user_data = Cls.get_user_info(access_token)
        contract = Cls.get_contract_instance(user_data)

        user = Cls.ServiceClass.get_user(contract)

        if not user:
            user = Cls.ServiceClass.register(contract)

        payload = Cls.get_payload(user)

        return Response(payload, 200)


    @classmethod
    def get_contract_instance(Cls, user_data):
        contract = Cls.ContractClass(
            username=user_data.get('email'),
            email=user_data.get('email'),
            first_name=user_data.get('given_name'),
            last_name=user_data.get('family_name'),
        )
        return contract

    @classmethod
    def get_payload(Cls, user_instance):
        # PAYLOAD POR NORMAL JWT PACKAGE

        # payload = jwt_payload_handler(user_instance)
        # token = jwt_encode_handler(payload)
        # payload['token'] = token

        # PAYLOAD FOR EASY JWT PACKAGE

        # refresh = RefreshToken.for_user(user_instance)
        # payload = {
        #     'refresh': str(refresh),
        #     'access': str(refresh.access_token)
        # }

        # PAYLOAD FOR CUSTOM AUTHORIZATION

        payload = Cls.JWTService.get_payload_from_user(user=user_instance)

        return payload


    @classmethod
    def get_user_info(Cls, access_token):
        headers = {'Authorization': 'Bearer ' + access_token}

        try:
            response = requests.get(
                'https://www.googleapis.com/oauth2/v2/userinfo', headers=headers)
        except (ConnectionError, Exception) as e:
            raise ThirdPartyServiceError(
                'Error connecting with Google Services') from e

        if status.is_client_error(response.status_code):
            raise AuthenticationFailed('Error with credentials')

        user_data = response.json()
        return user_data
