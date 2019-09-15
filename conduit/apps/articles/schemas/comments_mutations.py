import graphene
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from conduit.apps.articles.models import Article, Comment, Tag
from conduit.apps.core.database import SaveContextManager, get_model_object
from .articles_mutations import CommentType


class CommentsMutationCommons(graphene.Mutation):
    comment = graphene.Field(CommentType)
    message = graphene.String()

    class Arguments:
        id = graphene.Int()
        slug = graphene.String()
        body = graphene.String()

    def mutate(self, info, **kwargs):
        pass


class CreateComment(CommentsMutationCommons):

    @login_required
    def mutate(self, info, **kwargs):
        user_instance = info.context.user
        slug = kwargs.pop('slug', None)
        article_object = get_model_object(Article, 'slug', slug)
        success_message = "Commented on article {}".format(article_object.slug)
        comment = Comment(
            body=kwargs.pop('body', ""),
            article=article_object,
            author=user_instance.profile
        )
        with SaveContextManager(model_instance=comment) as comment:
            pass
        return CreateComment(comment=comment, message=success_message)


class UpdateComment(CommentsMutationCommons):

    @login_required
    def mutate(self, info, **kwargs):
        id = kwargs.get('id', None)
        comment = get_model_object(Comment, 'id', id)
        if info.context.user.profile == comment.author:
            params = {
                'body': kwargs.pop('body', comment.body),
            }
            for (key, value) in params.items():
                setattr(comment, key, value)
            success_message = "Comment updated successfully"
            with SaveContextManager(model_instance=comment) as comment:
                pass
            return UpdateComment(comment=comment, message=success_message)
        raise GraphQLError("You are not authorized to edit this comment")


class DeleteComment(CommentsMutationCommons):
    class Arguments:
        id = graphene.Int(required=True)

    def mutate(self, info, **kwargs):
        id = kwargs.get('id', None)
        comment = get_model_object(Comment, 'id', id)
        try:
            if info.context.user.profile == comment.author:
                comment.delete()
                return DeleteComment(message="Comment deleted successfully")
        except Exception as e:
            raise GraphQLError("error {}".format(str(e)))
        return DeleteComment(message="Comment deletion failed, you are not authorized to delete this comment")


class Mutation:
    create_comment = CreateComment.Field()
    update_comment = UpdateComment.Field()
    delete_comment = DeleteComment.Field()
