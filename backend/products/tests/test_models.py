from django.test import TestCase
from products.models import Brand, Product, Review, FavoriteProduct, CartProduct
from users.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError

class ProductTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(username="User1", email="User1@mail.ru")
        cls.user2 = User.objects.create_user(username="User2", email="User2@mail.ru")
        cls.product1 = Product.objects.create(name="Product1", description="description1", slug="product-1", price=1000)
        cls.product2 = Product.objects.create(name="Product2", description="description2", slug="product-2", price=2000)

    def test_clean_method_price_validation(self):
        self.product1.full_clean()

        product3 = Product(name="Test Product 3", description="description3", price=0, slug="product-3")
        with self.assertRaises(ValidationError):
            product3.full_clean()
        
        product4 = Product(name="Test Product 4", description="description3", price=-1, slug="product-4")
        with self.assertRaises(ValidationError) as context4:
            product4.full_clean()
        
        self.assertIn("Price should be a positive number", str(context4.exception))

    def test_get_rating_no_reviews(self):
        rating = self.product1.get_rating()
        self.assertIsNone(rating)

    def test_get_rating_one_review(self):
        Review.objects.create(product=self.product1, author=self.user1, rating=5, title="title", content="content")
        rating = self.product1.get_rating()
        self.assertEqual(rating, "5.0")
    
    def test_get_rating_two_reviews(self):
        Review.objects.create(product=self.product1, author=self.user1, rating=5, title="title", content="content")
        Review.objects.create(product=self.product1, author=self.user2, rating=4, title="title", content="content")
        rating = self.product1.get_rating()
        self.assertEqual(rating, "4.5")
  
    def test_get_review_amount_no_reviews(self):
        review_amount = self.product1.get_review_amount()
        self.assertEqual(review_amount, 0)
    
    def test_get_rating_one_review(self):
        Review.objects.create(product=self.product1, author=self.user1, rating=5, title="title", content="content")
        review_amount = self.product1.get_review_amount()
        self.assertEqual(review_amount, 1)
 
    def test_get_favorite_product_id_no_product(self):
        favorite_product_id = self.product1.get_favorite_product_id(self.user1)
        self.assertIsNone(favorite_product_id)
    
    def test_get_favorite_product_id_product_exists(self):
        self.favorite_product1 = FavoriteProduct.objects.create(user=self.user1, product=self.product1)
        favorite_product_id = self.product1.get_favorite_product_id(self.user1)
        self.assertEqual(favorite_product_id, self.favorite_product1.id)
 
    def test_get_cart_product_id_no_product(self):
        cart_product_id = self.product1.get_cart_product_id(self.user1)
        self.assertIsNone(cart_product_id)
    
    def test_get_cart_product_id_product_exists(self):
        self.cart_product1 = CartProduct.objects.create(user=self.user1, product=self.product1)
        cart_product_id = self.product1.get_cart_product_id(self.user1)
        self.assertEqual(cart_product_id, self.cart_product1.id)

    def test_get_is_favorite_product_false(self):
        self.assertFalse(self.product1.get_is_favorite_product(self.user1))

    def test_get_is_favorite_product_true(self):
        FavoriteProduct.objects.create(user=self.user1, product=self.product2)
        self.assertTrue(self.product2.get_is_favorite_product(self.user1))

    def test_get_is_cart_product_false(self):
        self.assertFalse(self.product1.get_is_cart_product(self.user1))

    def test_get_is_cart_product_true(self):
        CartProduct.objects.create(user=self.user1, product=self.product2)
        self.assertTrue(self.product2.get_is_cart_product(self.user1))

class CartProductTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="User1", email="User1@mail.ru")
        cls.product1 = Product.objects.create(name="Product1", slug="product-1", price=1000)
        cls.product2 = Product.objects.create(name="Product2", slug="product-2", price=2000)
        cls.cart_product1 = CartProduct.objects.create(user=cls.user, product=cls.product1)
        cls.cart_product2 = CartProduct.objects.create(user=cls.user, product=cls.product2)
    
    def test_get_product_price(self):
        self.assertEqual(self.cart_product1.get_product_price(), 1000)

    def test_get_total_quantity(self):
        self.assertEqual(self.cart_product1.get_total_quantity(self.user), 2)

    def test_get_total_price(self):
        self.assertEqual(self.cart_product1.get_total_price(self.user), 3000)