import factory
from faker import Faker
from conduit.apps.authentication.models import User
from conduit.apps.profiles.models import Profile
from conduit.apps.articles.models import Article, Comment
from django.db.models.signals import post_save

faker = Faker()


@factory.django.mute_signals(post_save)
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda x: "user_%d" % x)
    email = factory.Sequence(lambda x: "user%d@conduit.com" % x)
    password = faker.password(length=10, special_chars=True,
                              digits=True, upper_case=True,
                              lower_case=True)
    profile = factory.RelatedFactory('conduit.tests.factories.ProfileFactory', 'user')


@factory.django.mute_signals(post_save)
class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory, profile=None)
    bio = faker.text()


@factory.django.mute_signals(post_save)
class ArticleFactory(factory.DjangoModelFactory):
    class Meta:
        model = Article

    title = faker.sentences(nb=1, ext_word_list=None)[0]
    description = faker.text()
    body = faker.text()
    author = factory.SubFactory(ProfileFactory)

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for tag in extracted:
                self.tags.add(tag)


class CommentFactory(factory.DjangoModelFactory):
    class Meta:
        model = Comment

    body = faker.text()
    article = factory.SubFactory(ArticleFactory)
    author = factory.SubFactory(ProfileFactory)
