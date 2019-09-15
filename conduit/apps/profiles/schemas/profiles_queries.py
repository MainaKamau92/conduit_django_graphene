import graphene
from graphql import GraphQLError
from ..models import Profile
from .profiles_mutations import ProfileType
from graphql_jwt.decorators import login_required


class Query(graphene.ObjectType):
    profile = graphene.Field(ProfileType, id=graphene.Int(required=True))
    profiles = graphene.List(ProfileType)
    me = graphene.Field(ProfileType)

    @login_required
    def resolve_profiles(self, info):
        return Profile.objects.all()

    @login_required
    def resolve_profile(self, info, **kwargs):
        id = kwargs.get('id')
        try:
            return Profile.objects.get(pk=id)
        except:
            raise GraphQLError("Profile does not exist")

    @login_required
    def resolve_me(self, info, **kwargs):
        logged_in_user_profile = info.context.user if info.context.user.is_authenticated else None
        return Profile.objects.get(user=logged_in_user_profile)
