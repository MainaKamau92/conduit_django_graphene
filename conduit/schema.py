import graphene
from conduit.apps.authentication.schemas import AuthMutation, AuthQuery
from conduit.apps.profiles.schemas import ProfilesMutation, ProfilesQuery
from conduit.apps.articles.schemas import ArticlesMutation, ArticlesQuery, CommentMutation, CommentQuery


class Query(AuthQuery, ProfilesQuery, ArticlesQuery, CommentQuery, graphene.ObjectType):
    pass


class Mutation(AuthMutation, ProfilesMutation, ArticlesMutation, CommentMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
