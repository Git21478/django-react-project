import pytest
from products.serializers import (
    BrandSerializer, CategorySerializer, ProductSerializer,
    ReviewSerializer, FavoriteProductSerializer, FavoriteProductCreateSerializer,
    CartProductSerializer, CartProductCreateSerializer
)
from products.models import CartProduct

pytestmark = pytest.mark.django_db

class TestBrandSerializer:
    def test_brand_serializer_fields(self, brand1):
        serializer = BrandSerializer(brand1)
        
        assert set(serializer.data.keys()) == {"id", "name", "categories"}
        assert serializer.data["id"] == brand1.id
        assert serializer.data["name"] == "Brand 1"
        assert serializer.data["categories"] == []

    def test_brand_serializer_with_categories(self, brand1, category1):
        brand1.categories.add(category1)
        serializer = BrandSerializer(brand1)
        
        assert len(serializer.data["categories"]) == 1
        assert serializer.data["categories"][0]["id"] == category1.id
        assert serializer.data["categories"][0]["name"] == "Category 1"

    def test_brand_serializer_validation(self):
        serializer = BrandSerializer(data={"name": "Brand"})
        
        assert serializer.is_valid()
        assert serializer.validated_data["name"] == "Brand"

class TestCategorySerializer:
    def test_category_serializer_fields(self, category1):
        serializer = CategorySerializer(category1)
        
        assert set(serializer.data.keys()) == {"id", "name", "slug", "brands"}
        assert serializer.data["id"] == category1.id
        assert serializer.data["name"] == "Category 1"
        assert serializer.data["slug"] == "category-1"
        assert serializer.data["brands"] == []

    def test_category_serializer_with_brands(self, category1, brand1, brand2):
        category1.brands.add(brand1, brand2)
        serializer = CategorySerializer(category1)
        
        assert len(serializer.data["brands"]) == 2
        brand_names = [brand["name"] for brand in serializer.data["brands"]]
        assert "Brand 1" in brand_names
        assert "Brand 2" in brand_names

    def test_category_serializer_validation(self):
        data = {"name": "New Category", "slug": "new-category"}
        serializer = CategorySerializer(data=data)
        
        assert serializer.is_valid()
        assert serializer.validated_data["name"] == "New Category"
        assert serializer.validated_data["slug"] == "new-category"

class TestProductSerializer:
    def test_product_serializer_fields(self, product1, api_auth_client, user1):
        serializer = ProductSerializer(
            product1, 
            context={"request": api_auth_client.request}
        )
        
        expected_fields = {
            "id", "image", "name", "description", "price", 
            "category", "brand", "slug", "rating", "review_amount",
            "favorite_product_id", "cart_product_id", 
            "is_favorite_product", "is_cart_product"
        }
        assert set(serializer.data.keys()) == expected_fields
        
        assert serializer.data["id"] == product1.id
        assert serializer.data["name"] == "Product1"
        assert float(serializer.data["price"]) == 1000.00
        assert serializer.data["rating"] is None
        assert serializer.data["review_amount"] == 0
        assert serializer.data["favorite_product_id"] is None
        assert serializer.data["cart_product_id"] is None
        assert serializer.data["is_favorite_product"] is False
        assert serializer.data["is_cart_product"] is False

    def test_product_serializer_with_reviews(self, product1, review1, review2, api_auth_client):
        serializer = ProductSerializer(
            product1,
            context={"request": api_auth_client.request}
        )
        
        assert float(serializer.data["rating"]) == 4.5
        assert serializer.data["review_amount"] == 2

    def test_product_serializer_with_favorite(self, product1, favorite_product11, api_auth_client, user1):
        serializer = ProductSerializer(
            product1,
            context={"request": api_auth_client.request}
        )
        
        assert serializer.data["favorite_product_id"] == favorite_product11.id
        assert serializer.data["is_favorite_product"] is True

    def test_product_serializer_with_cart(self, product1, cart_product11, api_auth_client):
        serializer = ProductSerializer(
            product1,
            context={"request": api_auth_client.request}
        )
        
        assert serializer.data["cart_product_id"] == cart_product11.id
        assert serializer.data["is_cart_product"] is True

    def test_product_serializer_methods(self, product1, api_auth_client):
        serializer = ProductSerializer(
            product1,
            context={"request": api_auth_client.request}
        )
        
        assert serializer.data["rating"] == serializer.get_rating(product1)
        assert serializer.data["review_amount"] == serializer.get_review_amount(product1)

class TestReviewSerializer:
    def test_review_serializer_fields(self, review1, user1):
        serializer = ReviewSerializer(review1)
        
        expected_fields = {"id", "title", "content", "rating", "created_at", "author", "product"}
        assert set(serializer.data.keys()) == expected_fields
        
        assert serializer.data["id"] == review1.id
        assert serializer.data["title"] == "title1"
        assert serializer.data["content"] == "content1"
        assert serializer.data["rating"] == 5
        assert serializer.data["author"] == "User1"
        assert serializer.data["product"] == review1.product.id

    def test_review_serializer_validation_valid_data(self, product1, user1):
        data = {
            "title": "Test Review",
            "content": "Test Content",
            "rating": 4,
            "product": product1.id
        }
        serializer = ReviewSerializer(data=data)
        
        assert serializer.is_valid()

    def test_review_serializer_validation_rating_too_high(self, product1):
        data = {
            "title": "Test Review",
            "content": "Test Content",
            "rating": 6,
            "product": product1.id
        }
        serializer = ReviewSerializer(data=data)
        
        assert not serializer.is_valid()
        assert "rating" in serializer.errors

    def test_review_serializer_validation_rating_too_low(self, product1):
        data = {
            "title": "Test Review",
            "content": "Test Content",
            "rating": 0,
            "product": product1.id
        }
        serializer = ReviewSerializer(data=data)
        
        assert not serializer.is_valid()
        assert "rating" in serializer.errors

class TestFavoriteProductSerializer:
    def test_favorite_product_serializer_fields(self, favorite_product11):
        serializer = FavoriteProductSerializer(favorite_product11)
        
        assert set(serializer.data.keys()) == {"id", "user", "product"}
        assert serializer.data["id"] == favorite_product11.id
        assert serializer.data["user"] == favorite_product11.user.id
        assert "product" in serializer.data

    def test_favorite_product_serializer_nested_product(self, favorite_product11):
        serializer = FavoriteProductSerializer(favorite_product11)
        
        product_data = serializer.data["product"]
        assert "id" in product_data
        assert "name" in product_data
        assert "price" in product_data
        assert product_data["name"] == "Product1"

class TestFavoriteProductCreateSerializer:
    def test_favorite_create_serializer_fields(self):
        serializer = FavoriteProductCreateSerializer()
        
        assert set(serializer.fields.keys()) == {"id", "product"}

    def test_favorite_create_serializer_valid_data(self, product1, api_auth_client, user1):
        data = {"product": product1.id}
        serializer = FavoriteProductCreateSerializer(
            data=data,
            context={"request": api_auth_client.request}
        )
        
        assert serializer.is_valid()

    def test_favorite_create_serializer_duplicate_product(self, product1, favorite_product11, api_auth_client):
        data = {"product": product1.id}
        serializer = FavoriteProductCreateSerializer(
            data=data,
            context={"request": api_auth_client.request}
        )
        
        assert not serializer.is_valid()
        assert "non_field_errors" in serializer.errors
        assert "уже добавлен в избранное" in str(serializer.errors["non_field_errors"])

    def test_favorite_create_serializer_without_auth(self, product1, api_client):
        data = {"product": product1.id}
        serializer = FavoriteProductCreateSerializer(
            data=data,
            context={"request": api_client.request}
        )
        
        assert serializer.is_valid()

class TestCartProductSerializer:
    def test_cart_product_serializer_fields(self, cart_product11, api_auth_client):
        serializer = CartProductSerializer(
            cart_product11,
            context={"request": api_auth_client.request}
        )
        
        expected_fields = {"id", "user", "product", "quantity", "total_quantity", "total_price"}
        assert set(serializer.data.keys()) == expected_fields
        
        assert serializer.data["id"] == cart_product11.id
        assert serializer.data["user"] == cart_product11.user.id
        assert serializer.data["quantity"] == 1

    def test_cart_product_serializer_methods(self, cart_product11, api_auth_client, user1, product1, product2):
        CartProduct.objects.create(user=user1, product=product2, quantity=3)
        
        serializer = CartProductSerializer(
            cart_product11,
            context={"request": api_auth_client.request}
        )
        
        assert serializer.data["total_quantity"] == 4
        assert float(serializer.data["total_price"]) == 1000 + (2000 * 3)

    def test_cart_product_serializer_nested_product(self, cart_product11, api_auth_client):
        serializer = CartProductSerializer(
            cart_product11,
            context={"request": api_auth_client.request}
        )
        
        product_data = serializer.data["product"]
        assert "id" in product_data
        assert "name" in product_data
        assert "price" in product_data
        assert product_data["name"] == "Product1"

class TestCartProductCreateSerializer:
    def test_cart_create_serializer_fields(self):
        serializer = CartProductCreateSerializer()
        
        assert set(serializer.fields.keys()) == {"id", "product", "quantity"}

    def test_cart_create_serializer_valid_data(self, product1, api_auth_client):
        data = {"product": product1.id, "quantity": 3}
        serializer = CartProductCreateSerializer(
            data=data,
            context={"request": api_auth_client.request}
        )
        
        assert serializer.is_valid()

    def test_cart_create_serializer_without_quantity(self, product1, api_auth_client):
        data = {"product": product1.id}
        serializer = CartProductCreateSerializer(
            data=data,
            context={"request": api_auth_client.request}
        )
        
        assert serializer.is_valid()

    def test_cart_create_serializer_duplicate_product(self, product1, cart_product11, api_auth_client):
        data = {"product": product1.id, "quantity": 2}
        serializer = CartProductCreateSerializer(
            data=data,
            context={"request": api_auth_client.request}
        )
        
        assert not serializer.is_valid()
        assert "non_field_errors" in serializer.errors
        assert "уже добавлен в корзину" in str(serializer.errors["non_field_errors"])

    def test_cart_create_serializer_without_auth(self, product1, api_client):
        data = {"product": product1.id, "quantity": 2}
        serializer = CartProductCreateSerializer(
            data=data,
            context={"request": api_client.request}
        )
        
        assert serializer.is_valid()