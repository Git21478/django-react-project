import unittest
from django.test import TestCase
from products.models import Brand, Product, Review
from django.core.exceptions import ValidationError
from django.db import IntegrityError

class ProductModelTest(TestCase):
    def test_clean_method_price_validation(self):
        product1 = Product(name="Test Product 1", description="test product 1", price=1, slug="test_slug_1")
        product1.full_clean()

        product2 = Product(name="Test Product 2", description="test product 2", price=0, slug="test_slug_2")
        with self.assertRaises(ValidationError):
            product2.full_clean()
        
        product3 = Product(name="Test Product 3", description="test product 3", price=-1, slug="test_slug_3")
        with self.assertRaises(ValidationError) as context3:
            product3.full_clean()
        
        self.assertIn("Price should be a positive number", str(context3.exception))
    
    def test_get_rating(self):
        pass

class CartProductTest(TestCase):
    pass