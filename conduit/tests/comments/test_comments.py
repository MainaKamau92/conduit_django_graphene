from conduit.apps.core.generate_token import generate_token
from conduit.tests.base_config import BaseConfiguration
from conduit.tests.factories import ArticleFactory, CommentFactory, UserFactory
from conduit.tests.test_queries.comments import create_comment_mutation, update_comment_mutation, \
    delete_comment_mutation, get_all_comments_for_article


class CommentTestCase(BaseConfiguration):

    def setUp(self):
        super(CommentTestCase, self).setUp()
        self.test_article = ArticleFactory(slug="comment-edit-test-article")
        self.user = UserFactory()
        CommentFactory(article=self.test_article, author=self.user.profile)
        self.token = generate_token(self.user)

    def test_user_can_create_comment(self):
        ArticleFactory(slug="comment-test-article")
        response = self.query_with_token(self.access_token, create_comment_mutation.format(
            slug="comment-test-article",
            body="Test comment for an article"
        ))
        response_data = response.get("data")
        success_message = response_data["createComment"]["message"]
        comment_details = response_data["createComment"]["comment"]
        self.assertEqual(success_message, "Commented on article comment-test-article")
        self.assertEqual(comment_details["id"], str(2))

    def test_user_can_edit_comment(self):
        response = self.query_with_token(self.token, update_comment_mutation.format(
            id=1,
            body="updated comment body"
        ))
        response_data = response.get("data")
        success_message = response_data["updateComment"]["message"]
        edited_comment_body = response_data["updateComment"]["comment"]["body"]
        self.assertEqual(success_message, "Comment updated successfully")
        self.assertEqual(edited_comment_body, "updated comment body")

    def test_user_can_delete_comment(self):
        response = self.query_with_token(self.token, delete_comment_mutation.format(id=1))
        self.assertEqual(response["data"]["deleteComment"]["message"], "Comment deleted successfully")

    def test_user_can_get_all_comments_for_an_article(self):
        [CommentFactory(article=self.test_article, author=self.user.profile) for _ in range(0, 15)]
        response = self.query_with_token(self.token, get_all_comments_for_article.format(
            slug="comment-edit-test-article"
        ))
        response_data = response.get("data")
        self.assertEqual(len(response_data["articleComments"]), 16)
