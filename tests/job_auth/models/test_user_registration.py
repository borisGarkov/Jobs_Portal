from django.contrib.auth import get_user_model
from django.test import TestCase

UserModel = get_user_model()


class TestUserRegistration(TestCase):
    def setUp(self) -> None:
        self.user = UserModel.objects.create(email='test@test.com', username='test', password='test')

    def test_initialAttributes(self):
        self.assertEqual('test@test.com', self.user.email)
        self.assertEqual('test', self.user.username)
        self.assertEqual('test', self.user.password)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_active)
        self.assertFalse(self.user.is_superuser)
        self.assertEqual('test@test.com', str(self.user))
