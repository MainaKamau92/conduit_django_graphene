from graphene_django import DjangoObjectType
import graphene
from graphql_jwt.decorators import login_required

from ..models import Profile


class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile


class UpdateProfile(graphene.Mutation):
    profile = graphene.Field(ProfileType)
    message = graphene.String()

    class Arguments:
        name = graphene.String()
        bio = graphene.String()
        image = graphene.String()

    @login_required
    def mutate(self, info, **kwargs):
        user = info.context.user if info.context.user.is_authenticated else None
        profile_model = Profile.objects.get(user=user)
        if profile_model:
            for (key, value) in kwargs.items():
                if key is not None:
                    setattr(profile_model, key, value)
            profile_model.save()
            return UpdateProfile(profile=profile_model, message="Successfully updated your profile")
        return UpdateProfile(profile=profile_model, message="Error while updating profile")


class Mutation:
    update_profile = UpdateProfile.Field()
