import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from conduit.apps.articles.models import Article, Comment, Tag
from conduit.apps.core.database import SaveContextManager, get_model_object


class ArticleType(DjangoObjectType):
    class Meta:
        model = Article


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment


class TagType(DjangoObjectType):
    class Meta:
        model = Tag


class ArticleMutationCommons(graphene.Mutation):
    article = graphene.Field(ArticleType)
    message = graphene.String()

    class Arguments:
        slug = graphene.String()
        title = graphene.String()
        description = graphene.String()
        body = graphene.String()
        tags = graphene.List(graphene.String)

    def mutate(self, info, **kwargs):
        pass


class CreateArticle(ArticleMutationCommons):

    @login_required
    def mutate(self, info, **kwargs):
        user_instance = info.context.user
        tags = kwargs.pop('tags', [])
        success_message = "Article created successfully"
        article = Article(
            title=kwargs.pop('title', ""),
            description=kwargs.pop('description', ""),
            body=kwargs.pop('body', ""),
            author=user_instance.profile
        )
        with SaveContextManager(model_instance=article) as article:
            if len(tags) != 0:
                for tag in tags:
                    article.tags.create(tag=tag)
            return CreateArticle(article=article, message=success_message)


class UpdateArticle(ArticleMutationCommons):

    @login_required
    def mutate(self, info, **kwargs):
        slug = kwargs.pop('slug', None)
        tags = kwargs.pop('tags', [])
        article = get_model_object(Article, 'slug', slug)
        if info.context.user.profile == article.author:
            tags_list = article.tags.all()
            params = {
                'title': kwargs.pop('title', article.title),
                'description': kwargs.pop('description', article.description),
                'body': kwargs.pop('body', article.body),
            }
            for (key, value) in params.items():
                setattr(article, key, value)
            success_message = "Article updated successfully"
            with SaveContextManager(model_instance=article) as article:
                if len(tags) != 0:
                    [article.tags.create(tag=tag) for tag in tags if tag not in tags_list]
                return UpdateArticle(article=article, message=success_message)
        raise GraphQLError("You are not authorized to edit this article")


class FavoriteArticle(ArticleMutationCommons):
    class Arguments:
        slug = graphene.String(required=True)

    def mutate(self, info, **kwargs):
        user = info.context.user
        slug = kwargs.get('slug', None)
        article = get_model_object(Article, 'slug', slug)
        has_favorited = user.profile.has_favorited(article)
        if has_favorited:
            user.profile.unfavorite(article)
            return FavoriteArticle(article=article,
                                   message="Article of slug {}, has been unfavored".format(slug))
        user.profile.favorite(article)
        return FavoriteArticle(article=article,
                               message="Article of slug {}, has been added to favorites".format(slug))


class DeleteArticle(ArticleMutationCommons):
    class Arguments:
        slug = graphene.String(required=True)

    def mutate(self, info, **kwargs):
        slug = kwargs.get('slug', None)
        article = get_model_object(Article, 'slug', slug)
        try:
            if info.context.user.profile == article.author:
                article.delete()
                return DeleteArticle(message="Article deleted successfully")
        except Exception as e:
            raise GraphQLError("error {}".format(str(e)))
        return DeleteArticle(message="Article deletion failed, you are not authorized to delete this article")


class Mutation:
    create_article = CreateArticle.Field()
    update_article = UpdateArticle.Field()
    delete_article = DeleteArticle.Field()
    favorite_article = FavoriteArticle.Field()
