from conduit.tests.base_config import BaseConfiguration
from conduit.tests.factories import UserFactory
from conduit.tests.test_queries.authentication import register_user_query, login_user_query, get_all_users_query, \
    get_single_user_query


class UserTestCase(BaseConfiguration):

    def test_user_can_register(self):
        response = self.query(register_user_query.format(
            username="test_user",
            email="testuser@conduit.com",
            password="password123"
        ))
        data = response.get('data')
        self.assertEqual(data["registerUser"]["user"]["email"], "testuser@conduit.com")
        self.assertEqual(data["registerUser"]["successMessage"], "User created testuser@conduit.com successfully.")

    def test_user_can_login(self):
        self.test_user_can_register()
        response = self.query(login_user_query.format(
            email="testuser@conduit.com",
            password="password123"
        ))
        data = response.get('data')
        self.assertIn("token", data["loginUser"])
        self.assertIsNotNone(data["loginUser"]["success"])

    def test_user_can_get_all_registered_user(self):
        [UserFactory() for _ in range(0, 10)] #randomly generate 10 users for testing
        response = self.query_with_token(self.access_token, get_all_users_query)
        self.assertEqual(len(response["data"]["users"]), 11)

    def test_user_can_get_a_single_user(self):
        [UserFactory() for _ in range(0, 10)] #randomly generate 10 users for testing
        response = self.query_with_token(self.access_token, get_single_user_query.format(id=1))
        self.assertEqual(len(response), 1)









