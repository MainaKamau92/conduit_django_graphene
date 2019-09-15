from conduit.tests.base_config import BaseConfiguration
from conduit.tests.factories import ProfileFactory
from conduit.tests.test_queries.profiles import profile_update_mutation, get_all_profiles, get_single_profile


class ProfileTestCase(BaseConfiguration):
    
    def test_user_can_update_profile(self):
        response = self.query_with_token(self.access_token, profile_update_mutation.format(
            bio="This is the updated profile",
            name="R2D2",
            image="http://www.starwars.com/r2d2"
        ))
        response_data = response.get("data")
        updated_name = response_data["updateProfile"]["profile"]["name"]
        success_message  = response_data["updateProfile"]["message"]
        self.assertEqual(updated_name, "R2D2")
        self.assertEqual(success_message, "Successfully updated your profile")
    
    def test_user_can_fetch_all_available_profiles(self):
        [ProfileFactory() for _ in range(0, 10)]
        response = self.query_with_token(self.access_token, get_all_profiles)
        response_data = response.get("data")
        self.assertEqual(len(response_data["profiles"]), 11)
    
    def test_user_can_get_single_profile(self):
        response = self.query_with_token(self.access_token, get_single_profile.format(id=1))
        response_data = response.get("data")
        self.assertEqual(len(response_data), 1)