import pytest
from products.models import Brand, Category, Product, FavoriteProduct
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import ManyToManyField

@pytest.mark.django_db
class TestBrandModel:
    def test_create_brand(self, brand1):
        assert brand1.pk is not None
        assert brand1.name == "Brand 1"
    
    def test_brand_str_method(self, brand1):
        assert str(brand1) == "Brand 1"
    
    def test_brand_can_be_created_without_categories(self, brand1):
        assert brand1.categories.count() == 0

@pytest.mark.django_db
class TestCategoryModel:
    def test_create_category(self, category1):
        assert category1.pk is not None
        assert category1.name == "Category 1"
        assert category1.slug == "category-1"
    
    def test_category_str_method(self, category1):
        assert str(category1) == "Category 1"
    
    def test_category_slug_unique(self, category1):  
        with pytest.raises(IntegrityError):
            Category.objects.create(name="Category", slug="category-1")
    
    def test_category_brands_relation(self, brand1, brand2, brand3, category1):  
        category1.brands.add(brand1, brand2)
        
        assert category1.brands.count() == 2
        assert brand1 in category1.brands.all()
        assert brand2 in category1.brands.all()
        assert brand3 not in category1.brands.all()
    
    def test_category_brands_blank_true(self, category1):
        assert category1.brands.count() == 0
    
    def test_category_brands_related_name(self):
        field = Category._meta.get_field('brands')
        assert isinstance(field, ManyToManyField)
        assert field.remote_field.related_name == "categories"
        assert field.blank is True
    
    def test_reverse_relation_from_brand_to_categories(self, brand1, category1, category2):
        brand1.categories.add(category1, category2)
        
        assert brand1.categories.count() == 2
        assert category1 in brand1.categories.all()
        assert category2 in brand1.categories.all()

@pytest.mark.django_db
class TestBrandCategoryRelations:
    def test_many_to_many_relationship(self, brand1, brand2, brand3, category1, category2, category3):
        brand1.categories.add(category1, category2)
        brand2.categories.add(category2, category3)
        brand3.categories.add(category1, category3)
        
        assert brand1.categories.count() == 2
        assert brand2.categories.count() == 2
        assert brand3.categories.count() == 2
        
        assert category1.brands.count() == 2
        assert category2.brands.count() == 2
        assert category3.brands.count() == 2
        
        assert brand1 in category1.brands.all()
        assert brand3 in category1.brands.all()
        assert brand2 not in category1.brands.all()
    
    def test_delete_brand_does_not_delete_categories(self, brand1, category1):
        category1.brands.add(brand1)
        category_id = category1.pk
        brand1.delete()
        
        assert Category.objects.filter(pk=category_id).exists()
    
    def test_delete_category_does_not_delete_brands(self, brand1, category1):
        category1.brands.add(brand1)
        brand_id = brand1.pk
        category1.delete()
        
        assert Brand.objects.filter(pk=brand_id).exists()
    
    def test_clear_relationships(self, brand1, brand2, category1):
        category1.brands.add(brand1, brand2)
        assert category1.brands.count() == 2
        
        category1.brands.clear()
        assert category1.brands.count() == 0
        assert brand1.categories.count() == 0
        assert brand2.categories.count() == 0

@pytest.mark.django_db
class TestProduct:
    def test_clean_method_price_validation(self, product1):
        product1.full_clean()

        product3 = Product(name="Test Product 3", description="description3", price=0, slug="product-3")
        with pytest.raises(ValidationError):
            product3.full_clean()
        
        product4 = Product(name="Test Product 4", description="description3", price=-1, slug="product-4")
        with pytest.raises(ValidationError) as exception_info:
            product4.full_clean()
        
        assert "Price should be a positive number" in str(exception_info.value)

    def test_get_rating_no_reviews(self, product1):
        rating = product1.get_rating()
        assert rating is None

    def test_get_rating_one_review(self, user1, product1, review1):
        rating = product1.get_rating()
        assert rating == "5.0"
    
    def test_get_rating_two_reviews(self, user1, user2, product1, review1, review2):
        rating = product1.get_rating()
        assert rating == "4.5"
  
    def test_get_review_amount_no_reviews(self, product1):
        review_amount = product1.get_review_amount()
        assert review_amount == 0
    
    def test_get_review_amount_one_review(self, user1, product1, review1):
        review_amount = product1.get_review_amount()
        assert review_amount == 1
 
    def test_get_favorite_product_id_no_product(self, user1, product1):
        favorite_product_id = product1.get_favorite_product_id(user1)
        assert favorite_product_id is None
    
    def test_get_favorite_product_id_product_exists(self, user1, product1):
        favorite_product1 = FavoriteProduct.objects.create(user=user1, product=product1)
        favorite_product_id = product1.get_favorite_product_id(user1)
        assert favorite_product_id == favorite_product1.id
 
    def test_get_cart_product_id_no_product(self, user1, product1):
        cart_product_id = product1.get_cart_product_id(user1)
        assert cart_product_id is None
    
    def test_get_cart_product_id_product_exists(self, user1, product1, cart_product1):
        cart_product_id = product1.get_cart_product_id(user1)
        assert cart_product_id == cart_product1.id

    def test_get_is_favorite_product_false(self, user1, product1):
        assert not product1.get_is_favorite_product(user1)

    def test_get_is_favorite_product_true(self, user1, product2):
        FavoriteProduct.objects.create(user=user1, product=product2)
        assert product2.get_is_favorite_product(user1)

    def test_get_is_cart_product_false(self, user1, product1):
        assert not product1.get_is_cart_product(user1)

    def test_get_is_cart_product_true(self, user1, product2, cart_product2):
        assert product2.get_is_cart_product(user1)

@pytest.mark.django_db
class TestFavoriteProductModel:
    def test_create_favorite_with_user_and_product(self, user1, product1):
        favorite = FavoriteProduct.objects.create(user=user1, product=product1)
        assert favorite.pk is not None
        assert favorite.user == user1
        assert favorite.product == product1
    
    def test_create_favorite_without_user(self, product1):
        favorite = FavoriteProduct.objects.create(user=None, product=product1)
        assert favorite.pk is not None
        assert favorite.user is None
        assert favorite.product == product1
    
    def test_create_favorite_without_product(self, user1):
        with pytest.raises(IntegrityError):
            FavoriteProduct.objects.create(user=user1, product=None)
    
    def test_same_product_different_users(self, user1, user2, product1):
        fav1 = FavoriteProduct.objects.create(user=user1, product=product1)
        fav2 = FavoriteProduct.objects.create(user=user2, product=product1)
        
        assert fav1.pk != fav2.pk
        assert FavoriteProduct.objects.filter(product=product1).count() == 2
    
    def test_same_user_different_products(self, user1, product1, product2):
        fav1 = FavoriteProduct.objects.create(user=user1, product=product1)
        fav2 = FavoriteProduct.objects.create(user=user1, product=product2)
        
        assert fav1.pk != fav2.pk
        assert FavoriteProduct.objects.filter(user=user1).count() == 2
    
    def test_str_method(self, user1, product1):
        favorite = FavoriteProduct.objects.create(user=user1, product=product1)
        expected_str = product1.name
        assert str(favorite) == expected_str
    
    def test_str_method_without_user(self, product1):
        favorite = FavoriteProduct.objects.create(user=None, product=product1)
        expected_str = product1.name
        assert str(favorite) == expected_str
    
    def test_verbose_names(self):
        assert FavoriteProduct._meta.verbose_name == "Избранный товар"
        assert FavoriteProduct._meta.verbose_name_plural == "Избранные товары"
        
        user_field = FavoriteProduct._meta.get_field('user')
        assert user_field.verbose_name == "Пользователь"
        assert user_field.blank is True
        assert user_field.null is True
        
        product_field = FavoriteProduct._meta.get_field('product')
        assert product_field.verbose_name == "Товар"
        assert product_field.blank is False
        assert product_field.null is False
    
    def test_related_names(self):
        user_field = FavoriteProduct._meta.get_field('user')
        assert user_field.remote_field.related_name == "favorite_products"
        
        product_field = FavoriteProduct._meta.get_field('product')
        assert product_field.remote_field.related_name == "favorite_products"
    
    def test_cascade_delete_user(self, user1, product1):
        favorite = FavoriteProduct.objects.create(user=user1, product=product1)
        fav_id = favorite.pk
        
        user1.delete()
        assert not FavoriteProduct.objects.filter(pk=fav_id).exists()
    
    def test_cascade_delete_product(self, user1, product1):
        favorite = FavoriteProduct.objects.create(user=user1, product=product1)
        fav_id = favorite.pk
        
        product1.delete()
        assert not FavoriteProduct.objects.filter(pk=fav_id).exists()
    
    def test_filter_by_user(self, user1, user2, product1, product2):
        FavoriteProduct.objects.create(user=user1, product=product1)
        FavoriteProduct.objects.create(user=user1, product=product2)
        FavoriteProduct.objects.create(user=user2, product=product1)
        
        user1_favorites = FavoriteProduct.objects.filter(user=user1)
        assert user1_favorites.count() == 2
        
        user2_favorites = FavoriteProduct.objects.filter(user=user2)
        assert user2_favorites.count() == 1
    
    def test_filter_by_product(self, user1, user2, product1, product2):
        FavoriteProduct.objects.create(user=user1, product=product1)
        FavoriteProduct.objects.create(user=user1, product=product2)
        FavoriteProduct.objects.create(user=user2, product=product1)
        
        product1_favorites = FavoriteProduct.objects.filter(product=product1)
        assert product1_favorites.count() == 2
        
        product2_favorites = FavoriteProduct.objects.filter(product=product2)
        assert product2_favorites.count() == 1
    
    def test_user_favorite_products_relation(self, user1, product1, product2):
        fav1 = FavoriteProduct.objects.create(user=user1, product=product1)
        fav2 = FavoriteProduct.objects.create(user=user1, product=product2)
        
        assert user1.favorite_products.count() == 2
        assert fav1 in user1.favorite_products.all()
        assert fav2 in user1.favorite_products.all()
    
    def test_product_favorite_products_relation(self, user1, user2, product1):
        fav1 = FavoriteProduct.objects.create(user=user1, product=product1)
        fav2 = FavoriteProduct.objects.create(user=user2, product=product1)
        
        assert product1.favorite_products.count() == 2
        assert fav1 in product1.favorite_products.all()
        assert fav2 in product1.favorite_products.all()

@pytest.mark.django_db
class TestCartProduct:
    def test_get_product_price(self, cart_product1):
        assert cart_product1.get_product_price() == 1000

    def test_get_total_quantity(self, user1, cart_product1, cart_product2):
        assert cart_product1.get_total_quantity(user1) == 2

    def test_get_total_price(self, user1, cart_product1, cart_product2):
        assert cart_product1.get_total_price(user1) == 3000