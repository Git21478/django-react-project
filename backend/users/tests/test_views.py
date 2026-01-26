import unittest
from django.test import TestCase
from users.models import User

class HomePageTest(TestCase):
    @unittest.skip("")
    def test_anonymous_users_access(self):
        response = self.client.get("/http://localhost:5173/")
        self.assertRedirects(response, expected_url="/login/")

    def test_authenticated_users_access(self):
        User.objects.create_user(username="testuser", password="testpassword")
        self.client.login(username="testuser", password="testpassword")