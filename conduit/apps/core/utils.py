import re
from graphql import GraphQLError
import random
import string

DEFAULT_CHAR_STRING = string.ascii_lowercase + string.digits

class Validation:

    def validate_data_fields(self, username, email, password):
        return dict(email=self.validate_email(email),
                    username=self.validate_username(username),
                    password=self.validate_password(password))

    @staticmethod
    def validate_email(email):
        try:
            match = re.search(
                r'\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b', email, re.I)
            return match.group()
        except:
            raise GraphQLError("Invalid email")

    @staticmethod
    def validate_password(password):
        try:
            match = re.match(r'[A-Za-z0-9@#$%^&+_*()=]{8,}', password, re.I)
            return match.group()
        except:
            raise GraphQLError("Invalid password")

    @staticmethod
    def validate_username(username):
        try:
            match = re.match(r'^[a-zA-Z0-9_.-]+$', username, re.I)
            return match.group()
        except:
            raise GraphQLError("Invalid username")



def generate_random_string(chars=DEFAULT_CHAR_STRING, size=6):
    return ''.join(random.choice(chars) for _ in range(size))
