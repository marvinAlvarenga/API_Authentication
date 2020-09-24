from .contracts import UserContract
from .models import User


class UserService():
    @classmethod
    def register(cls, user_contract):
        if not isinstance(user_contract, UserContract):
            raise TypeError('\'user_contract\' variable must be an UserContract instance')

        user = User.objects.create(
            username=user_contract.username,
            email=user_contract.email,
            first_name=user_contract.first_name,
            last_name=user_contract.last_name,
        )

        return user

    @classmethod
    def get_user(cls, user_contract):
        if not isinstance(user_contract, UserContract):
            raise TypeError('\'user_contract\' variable must be an UserContract instance')

        try:
            user = User.objects.get(username=user_contract.username)

        except User.DoesNotExist:
            return None

        return user
