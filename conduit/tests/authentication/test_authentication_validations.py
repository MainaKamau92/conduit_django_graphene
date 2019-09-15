from conduit.tests.base_config import BaseConfiguration
from conduit.apps.core.utils import Validation


class TestValidationCase(BaseConfiguration):
    def test_email_validation(self):
        email_validator = Validation.validate_email(email="test@user.com")
        self.assertEquals(email_validator, "test@user.com")

    def test_password_validation(self):
        email_validator = Validation.validate_password(password="Tester123")
        self.assertEquals(email_validator, "Tester123")

    def test_username_validation(self):
        email_validator = Validation.validate_username("tester")
        self.assertEquals(email_validator, "tester")
