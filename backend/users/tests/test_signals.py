from django.test import TestCase
from users.models import User, Profile

class UserCreationSignalsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email="test123@test.ru", username="test123", password="test123")

    def test_profile_creation(self):
        profile = Profile.objects.get(user = self.user.id)
        self.assertTrue(profile)