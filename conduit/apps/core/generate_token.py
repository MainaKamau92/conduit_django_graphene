from graphql_jwt.utils import jwt_payload, jwt_encode


def generate_token(user):
    token = jwt_encode(jwt_payload(user))
    return token
