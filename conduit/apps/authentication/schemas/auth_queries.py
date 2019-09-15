import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from ..models import User
from graphql_jwt.decorators import login_required


class UserType(DjangoObjectType):
    class Meta:
        model = User


class Query(graphene.ObjectType):
    user = graphene.Field(UserType, id=graphene.Int(required=True))
    users = graphene.List(UserType)

    @login_required
    def resolve_users(self, info):
        return User.objects.all()

    @login_required
    def resolve_user(self, info, **kwargs):
        id = kwargs.get('id')
        try:
            return User.objects.get(pk=id)
        except:
            raise GraphQLError("User does not exist")
