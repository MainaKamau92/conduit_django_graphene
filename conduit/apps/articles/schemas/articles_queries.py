import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from conduit.apps.core.database import get_model_object
from ..models import Article
from graphql_jwt.decorators import login_required
from .articles_mutations import ArticleType


class Query(graphene.ObjectType):
    article = graphene.Field(ArticleType, slug=graphene.String(required=True))
    articles = graphene.List(ArticleType)
    article_feed = graphene.List(ArticleType)

    @login_required
    def resolve_articles(self, info):
        return Article.objects.all()

    @login_required
    def resolve_article(self, info, **kwargs):
        slug = kwargs.get('slug')
        try:
            return get_model_object(Article, 'slug', slug)
        except:
            raise GraphQLError("Article does not exist")

    @login_required
    def resolve_article_feed(self, info, **kwargs):
        return Article.objects.filter(
            author__in=info.context.user.profile.follows.all()
        )


