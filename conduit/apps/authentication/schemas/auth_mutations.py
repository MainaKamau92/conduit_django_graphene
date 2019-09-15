import graphene

from conduit.apps.core.database import SaveContextManager
from ..models import User
from .auth_queries import UserType
from conduit.apps.core.utils import Validation
from django.contrib.auth import authenticate
from conduit.apps.core.generate_token import generate_token

class RegisterUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String()
        email = graphene.String()
        password = graphene.String()

    errors = graphene.String()
    success_message = graphene.String()
    token = graphene.String()

    def mutate(self, info, **kwargs):
        username = kwargs.get('username')
        email = kwargs.get('email')
        password = kwargs.get('password')

        validate_data = Validation().validate_data_fields(
            username, email, password)
        user = User(**validate_data)
        message = "User created {} successfully.".format(email)
        with SaveContextManager(model_instance=user) as user:
            user.set_password(kwargs.get('password'))
            user.save()
            return RegisterUser(user=user, success_message=message, token=generate_token(user))


class LoginUser(graphene.Mutation):
    user = graphene.Field(UserType)
    errors = graphene.String()
    token = graphene.String()
    success = graphene.String()

    class Arguments:
        email = graphene.String()
        password = graphene.String()

    def mutate(self, info, **kwargs):
        email = Validation.validate_email(email=kwargs.get('email'))
        password = Validation.validate_password(
            password=kwargs.get('password'))

        user = authenticate(username=email, password=password)

        error_message = 'Invalid login credentials'
        success_message = 'Login successful'
        if user:
            token = generate_token(user)
            return LoginUser(user=user, token=token, success=success_message)
        return LoginUser(errors=error_message)




class Mutation(graphene.ObjectType):
    register_user = RegisterUser.Field()
    login_user = LoginUser.Field()
