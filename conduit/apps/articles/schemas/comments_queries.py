import graphene
from conduit.apps.core.database import get_model_object
from ..models import Article
from graphql_jwt.decorators import login_required
from .articles_mutations import CommentType, Comment


class Query(graphene.ObjectType):
    article_comments = graphene.List(CommentType, slug=graphene.String(required=True))

    @login_required
    def resolve_article_comments(self, info, **kwargs):
        slug = kwargs.get('slug', None)
        article_object = get_model_object(Article, 'slug', slug)
        return Comment.objects.filter(article=article_object)

