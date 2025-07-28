import unittest
from django.test import TestCase
from .models import Product, Review
from django.core.exceptions import ValidationError
from django.db import IntegrityError

class ProductModelTest(TestCase):
    def test_negative_price_constraint(self):
        product = Product(name="Test Product", description="test product", price=-1000)
        with self.assertRaises(IntegrityError):
            product.save()
    
    def test_zero_price_constraint(self):
        product = Product(name="Test Product", description="test product", price=0)
        with self.assertRaises(IntegrityError):
            product.save()

class ReviewModelTest(TestCase):  
    def test_review_rating_higher_than_5(self):
        review = Review(title="Test review", content="Lorem ipsum dolor sit amet, consectetur adipiscing elit.", rating=6)
        self.assertFalse(review.rating <= 5)
    
    def test_review_rating_lower_than_1(self):
        review = Review(title="Test review", content="Lorem ipsum dolor sit amet, consectetur adipiscing elit.", rating=0)
        self.assertFalse(review.rating >= 1)