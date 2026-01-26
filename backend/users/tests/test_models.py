import unittest
from django.test import TestCase
from users.models import User, Profile
from django.core.exceptions import ValidationError
from django.db import IntegrityError

class UserModelTest(TestCase):
    @unittest.skip("")
    def test_user_creation_not_unique(self):
        User.objects.create_user(email="test123@test.ru", username="test123", password="test123")
        with self.assertRaises(IntegrityError):
            User.objects.create_user(email="test123@test.ru", username="test123", password="test123")

class ProfileModelTest(TestCase):
    @unittest.skip("")
    def test_profile_update_phone_constraint(self):
        user = User.objects.create_user(email="test123@test.ru", username="test123", password="test123")
        profile = Profile.objects.get(user=user.id) # phone="+79182511265"
        profile.phone = "+7918251126500000000"
        with self.assertRaises(IntegrityError):
            profile.save()