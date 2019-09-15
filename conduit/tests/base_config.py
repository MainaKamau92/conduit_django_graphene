import json
from django.test import Client, TestCase
from .factories import UserFactory
from conduit.apps.core.generate_token import generate_token

GRAPHQL_ENDPOINT = '/conduit/'


class BaseConfiguration(TestCase):

    def setUp(self):
        """
        Configurations to be made available before each
        individual test case inheriting from this class.
        """
        self.client = Client()
        self.user = UserFactory()
        self.access_token = generate_token(self.user)


    def query(self, query: str = None):
        # Method to run all queries and mutations for tests.
        body = dict()
        body['query'] = query
        response = self.client.post(
            GRAPHQL_ENDPOINT, json.dumps(body),
            content_type='application/json')
        json_response = json.loads(response.content.decode())
        return json_response

    def query_with_token(self, access_token, query: str = None):
        # Method to run queries and mutations using a logged in user
        # with an authentication token
        body = dict()
        body['query'] = query
        http_auth = 'JWT {}'.format(access_token)
        url = GRAPHQL_ENDPOINT
        content_type = 'application/json'

        response = self.client.post(
            url,
            json.dumps(body),
            HTTP_AUTHORIZATION=http_auth,
            content_type=content_type)

        json_response = json.loads(response.content.decode())
        return json_response



    #
