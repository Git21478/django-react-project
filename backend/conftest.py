import pytest
from rest_framework.test import APIClient
from products.models import Brand, Category, Product, Review, FavoriteProduct, CartProduct
from users.models import User
from django.urls import reverse

@pytest.fixture
def user1(db):
    return User.objects.create_user(username="User1", email="User1@mail.ru", password="testpassword123")
@pytest.fixture
def user2(db):
    return User.objects.create_user(username="User2", email="User2@mail.ru", password="testpassword123")

@pytest.fixture
def api_client(db):
    return APIClient()
@pytest.fixture
def api_auth_client(db, api_client, user1):
    api_client.force_authenticate(user=user1)
    return api_client

@pytest.fixture
def brand1(db):
    return Brand.objects.create(name="Brand 1")
@pytest.fixture
def brand2(db):
    return Brand.objects.create(name="Brand 2")
@pytest.fixture
def brand3(db):
    return Brand.objects.create(name="Brand 3")

@pytest.fixture
def category1(db):
    return Category.objects.create(name="Category 1", slug="category-1")
@pytest.fixture
def category2(db):
    return Category.objects.create(name="Category 2", slug="category-2")
@pytest.fixture
def category3(db):
    return Category.objects.create(name="Category 3", slug="category-3")

@pytest.fixture
def product1(db):
    return Product.objects.create(name="Product1", description="description1", slug="product-1", price=1000)
@pytest.fixture
def product2(db):
    return Product.objects.create(name="Product2", description="description2", slug="product-2", price=2000)

@pytest.fixture
def review1(db, user1, product1):
    return Review.objects.create(product=product1, author=user1, rating=5, title="title1", content="content1")
@pytest.fixture
def review2(db, user2, product1):
    return Review.objects.create(product=product1, author=user2, rating=4, title="title2", content="content2")

@pytest.fixture
def favorite_product11(db, user1, product1):
    return FavoriteProduct.objects.create(user=user1, product=product1)
@pytest.fixture
def favorite_product12(db, user1, product2):
    return FavoriteProduct.objects.create(user=user1, product=product2)
@pytest.fixture
def favorite_product21(db, user2, product1):
    return FavoriteProduct.objects.create(user=user2, product=product1)
@pytest.fixture
def favorite_product22(db, user2, product2):
    return FavoriteProduct.objects.create(user=user2, product=product2)

@pytest.fixture
def cart_product1(db, user1, product1):
    return CartProduct.objects.create(user=user1, product=product1)
@pytest.fixture
def cart_product2(db, user1, product2):
    return CartProduct.objects.create(user=user1, product=product2)



@pytest.fixture
def url_category1(db, category1):
    return reverse("category-brands", kwargs={"category": category1.id})
@pytest.fixture
def url_category2(db, category2):
    return reverse("category-brands", kwargs={"category": category2.id})

@pytest.fixture
def url_category_list(db):
    return reverse("category-list")

@pytest.fixture
def url_product_list(db):
    return reverse("product-list")
@pytest.fixture
def url_product_category_list(db, category1):
    return reverse("product-category-list", kwargs={"pk": category1.pk})
@pytest.fixture
def url_product_retrieve_change_delete(db, product1):
    return reverse("product-retrieve-change-delete", kwargs={"pk": product1.pk})

@pytest.fixture
def url_review_list_create(db, product1):
    return reverse("product-review-list-create", kwargs={"product_id": product1.id})
@pytest.fixture
def url_review_detail(db, review1):
    return reverse("product-review", kwargs={"pk": review1.pk})

@pytest.fixture
def url_favorite_product_list_create(db):
    return reverse("favorite-product-list-create")
@pytest.fixture
def url_favorite_product(db):
    def _get_url(pk):
        return reverse("favorite-product", kwargs={"pk": pk})
    return _get_url
@pytest.fixture
def url_favorite_product_delete_multiple(db):
    def _get_url(*ids):
        ids_str = ",".join(str(id) for id in ids)
        return f"{reverse("favorite-product-delete-multiple")}?ids={ids_str}"
    return _get_url