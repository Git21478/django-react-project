from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from users.models import User
from products.models import Brand, Category, Product
from products.serializers import BrandSerializer
from decimal import Decimal
from products.views import ReviewPaginationPages
from django.core.exceptions import ValidationError

class BrandCategoryListTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(username="User", email="User@mail.ru", password="testpassword123")

        self.category1 = Category.objects.create(name="Category 1", slug="category-1")
        self.category2 = Category.objects.create(name="Category 2", slug="category-2")

        self.brand1 = Brand.objects.create(name="Brand 1")
        self.brand1.categories.add(self.category1)

        self.brand2 = Brand.objects.create(name="Brand 2")
        self.brand2.categories.add(self.category1)

        self.brand3 = Brand.objects.create(name="Brand 3")
        self.brand3.categories.add(self.category2)

        self.url_category1 = reverse("category-brands", kwargs={"category": self.category1.id})
        self.url_category2 = reverse("category-brands", kwargs={"category": self.category2.id})
     
    def test_brand_category_list_unauthorized_access(self):
        response = self.client.get(self.url_category1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_brand_category_list_authorized_access(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url_category1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_brand_category_list_returns_correct_brands(self):
        response = self.client.get(self.url_category1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        brands = [brand["name"] for brand in response.data]
        self.assertIn("Brand 1", brands)
        self.assertIn("Brand 2", brands)
        self.assertNotIn("Brand 3", brands)

        response = self.client.get(self.url_category2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        brands = [brand["name"] for brand in response.data]
        self.assertNotIn("Brand 1", brands)
        self.assertNotIn("Brand 2", brands)
        self.assertIn("Brand 3", brands)
    
    def test_brand_category_list_nonexistent_category(self):
        url = reverse("category-brands", kwargs={"category": 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_brand_category_list_empty_category(self):
        category3 = Category.objects.create(name="Category 3", slug="category-3")
        url = reverse("category-brands", kwargs={"category": category3.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
    
    def test_brand_category_list_brand_in_multiple_categories(self):
        self.brand1.categories.add(self.category2)

        response = self.client.get(self.url_category1)
        brand_names = [brand["name"] for brand in response.data]
        self.assertIn("Brand 1", brand_names)

        response = self.client.get(self.url_category2)
        brand_names = [brand["name"] for brand in response.data]
        self.assertIn("Brand 1", brand_names)

    def test_brand_category_list_response_format(self):
        response = self.client.get(self.url_category1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        brand_data = response.data[0]
        self.assertIn("id", brand_data)
        self.assertIn("name", brand_data)

class CategoryListTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.anonymous_client = APIClient()
        self.user = User.objects.create_user(username="User", email="User@mail.ru", password="testpassword123")
        self.category1 = Category.objects.create(name="Category 1", slug="category-1")
        self.category2 = Category.objects.create(name="Category 2", slug="category-2")
        self.category3 = Category.objects.create(name="Category 3", slug="category-3")
        self.list_url = reverse("category-list")
    
    def test_category_list_unauthorized_read_access(self):
        response = self.anonymous_client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_category_list_authorized_read_access(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_category_list_unauthorized_write_access(self):
        data = {"name": "New Category", "slug": "new-category"}
        
        response = self.anonymous_client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        response = self.anonymous_client.put(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_category_list_authorized_write_access_not_allowed(self):
        self.client.force_authenticate(user=self.user)
        data = {"name": "New Category", "slug": "new-category"}
        
        response = self.client.post(self.list_url, data)
    
    def test_category_list_returns_all_categories(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        category_names = [category["name"] for category in response.data]
        self.assertIn("Category 1", category_names)
        self.assertIn("Category 2", category_names)
        self.assertIn("Category 3", category_names)

class ProductTests(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Category")
        self.brand = Brand.objects.create(name="Brand")
        self.product = Product.objects.create(name="Product", price=Decimal("99.99"), category=self.category, brand=self.brand)
    
    def test_product_list_pagination(self):
        url = reverse("product-list")
        response = self.client.get(url, {"page": 1, "pageSize": 5})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertIn("count", response.data)
    
    def test_product_list_search(self):
        url = reverse("product-list")
        response = self.client.get(url, {"search": "Test"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_product_category_filter(self):
        url = reverse("product-category-list", kwargs={"pk": self.category.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_product_price_range_validation(self):
        url = reverse("product-category-list", kwargs={"pk": self.category.pk})   

        with self.assertRaises(ValidationError) as context:
            self.client.get(url, {'price_min': 'abc', 'price_max': 'xyz'})
        error_message = str(context.exception)
        self.assertIn('должно быть десятичным числом', error_message)
        
        response = self.client.get(url, {"price_min": "10", "price_max": "100"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_product_brand_filter(self):
        url = reverse("product-category-list", kwargs={"pk": self.category.pk})
        response = self.client.get(url, {"selected_brands_ids": self.brand.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_product_invalid_brand_ids(self):
        url = reverse("product-category-list", kwargs={"pk": self.category.pk})
        response = self.client.get(url, {"selected_brands_ids": "a,b,c"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_product_ordering(self):
        url = reverse("product-list")
        response = self.client.get(url, {"ordering": "price"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response = self.client.get(url, {"ordering": "-price"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_product_retrieve(self):
        url = reverse("product-retrieve-change-delete", kwargs={"pk": self.product.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.product.name)
    
    def test_product_update_permissions(self):
        url = reverse("product-retrieve-change-delete", kwargs={"pk": self.product.pk})
        data = {"name": "Updated Product Name"}
        
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class ReviewPaginationTests(APITestCase):
    def test_pagination_attributes(self):
        pagination = ReviewPaginationPages()

        self.assertEqual(pagination.page_query_param, "page")
        self.assertEqual(pagination.page_size, 10)
        self.assertEqual(pagination.page_size_query_param, "pageSize")
        self.assertEqual(pagination.max_page_size, 100)

class ReviewListCreateTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username="User1", email="User1@mail.ru", password="testpassword123")
        self.user2 = User.objects.create_user(username="User2", email="User2@mail.ru", password="testpassword123")
        self.product = Product.objects.create(name="Test Product", price=100.00)
        self.url = reverse("review-list-create", kwargs={"product_id": self.product.id})
        
        Review.objects.create(product=self.product, author=self.user1, rating=4, content="content1")
        Review.objects.create(product=self.product, author=self.user2, rating=5, content="content2")

class ReviewRetrieveUpdateDestroyTests(APITestCase):
    pass