from django.contrib.auth import get_user_model
from django.test import TestCase

from jobs_portal.profiles.models import ProfileModel

UserModel = get_user_model()


class TestProfile(TestCase):
    def setUp(self) -> None:
        self.user = UserModel.objects.create(email='test@test.com', username='test', password='test')
        self.profile = self.user.profilemodel

    def test_userProfileInitialAttributes(self):
        self.assertEqual(None, self.profile.first_name)
        self.assertEqual(None, self.profile.last_name)
        self.assertEqual(None, self.profile.profession)
        self.assertEqual(None, self.profile.website_url)
        self.assertEqual(None, self.profile.facebook_url)
        self.assertEqual(None, self.profile.instagram_url)
        self.assertEqual(None, self.profile.twitter_url)
        self.assertEqual(None, self.profile.twitter_url)
        self.assertEqual('None None - User (test@test.com)', str(self.profile))
