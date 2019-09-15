from conduit.tests.base_config import BaseConfiguration
from conduit.tests.factories import ArticleFactory, UserFactory
from conduit.tests.test_queries.articles import create_article_mutation, get_all_articles, get_single_article, \
    update_article_mutation, delete_article_mutation, favorite_article_mutation


class ArticleTestCase(BaseConfiguration):

    def test_user_can_create_article(self):
        response = self.query_with_token(self.access_token, create_article_mutation.format(
            title="article test user 5",
            description="This is a new article by test user 5",
            body="Lorem ipsum dolor sit amet, consectetur adipisicing elit."
                 "Blanditiis ducimus earum in laboriosam maxime nihil perferendis"
                 "quibusdamrem sint, sunt. Distinctio doloremqueexercitationem ipsa"
                 "laboriosam libero molestiae quasi quis, quos?",
            lorem="lorem",
            ipsum="ipsum"
        ))
        response_data = response.get("data")
        created_title = response_data["createArticle"]["article"]["title"]
        success_message = response_data["createArticle"]["message"]
        self.assertEqual(created_title, "article test user 5")
        self.assertEqual(success_message, "Article created successfully")

    def test_user_can_update_article(self):
        from conduit.apps.core.generate_token import generate_token
        user = UserFactory(username="test_user")
        token = generate_token(user)
        ArticleFactory(slug="test-article-123", author=user.profile)
        response = self.query_with_token(token, update_article_mutation.format(
            slug="test-article-123",
            title="edited conduit article title",
        ))
        response_data = response.get("data")
        updated_title = response_data["updateArticle"]["article"]["title"]
        success_message = response_data["updateArticle"]["message"]
        self.assertEqual(updated_title, "edited conduit article title")
        self.assertEqual(success_message, "Article updated successfully")

    def test_user_can_delete_an_article(self):
        from conduit.apps.core.generate_token import generate_token
        user = UserFactory(username="test_user")
        token = generate_token(user)
        ArticleFactory(slug="test-article-123", author=user.profile)
        response = self.query_with_token(token, delete_article_mutation.format(
            slug="test-article-123",
        ))
        response_data = response.get("data")
        success_message = response_data["deleteArticle"]["message"]
        self.assertEqual(success_message, "Article deleted successfully")

    def test_user_can_favorite_article(self):
        ArticleFactory(slug="favorite-article-123")
        response = self.query_with_token(self.access_token, favorite_article_mutation.format(
            slug="favorite-article-123"
        ))
        response_data = response.get("data")
        success_message = response_data["favoriteArticle"]["message"]
        favoring_username = response_data["favoriteArticle"]["article"]["favoritedBy"][0]["user"]["username"]
        self.assertEqual(success_message, "Article of slug favorite-article-123, has been added to favorites")
        self.assertEqual(favoring_username, self.user.username)

    def test_user_can_get_all_articles(self):
        [ArticleFactory() for _ in range(0, 10)]
        response = self.query_with_token(self.access_token, get_all_articles)
        response_data = response.get("data")
        self.assertEqual(len(response_data["articles"]), 10)

    def test_user_can_get_single_article(self):
        ArticleFactory(slug="new-article-123")
        response = self.query_with_token(self.access_token, get_single_article.format(slug="new-article-123"))
        response_data = response.get("data")
        self.assertEqual(response_data["article"]["slug"], "new-article-123")
        self.assertEqual(len(response_data), 1)
