import pytest
from rest_framework import status
from django.urls import reverse
from products.models import Review, FavoriteProduct
from products.views import ReviewPaginationPages
from django.core.exceptions import ValidationError
from django.db import IntegrityError

# @pytest.mark.django_db
# class TestBrandCategoryList:
#     def test_brand_category_list_unauthorized_access(self, api_client, url_category1):
#         response = api_client.get(url_category1)
#         assert response.status_code == status.HTTP_200_OK

#     def test_brand_category_list_authorized_access(self, api_auth_client, url_category1):
#         response = api_auth_client.get(url_category1)
#         assert response.status_code == status.HTTP_200_OK
    
#     def test_brand_category_list_returns_correct_brands(self, api_client, brand1, brand2, brand3, category1, category2, url_category1, url_category2):
#         brand1.categories.add(category1)
#         brand2.categories.add(category1)
#         brand3.categories.add(category2)

#         response = api_client.get(url_category1)
#         assert response.status_code == status.HTTP_200_OK
#         assert len(response.data) == 2

#         brands = [brand["name"] for brand in response.data]
#         assert "Brand 1" in brands
#         assert "Brand 2" in brands
#         assert "Brand 3" not in brands

#         response = api_client.get(url_category2)
#         assert response.status_code == status.HTTP_200_OK
#         assert len(response.data) == 1

#         brands = [brand["name"] for brand in response.data]
#         assert "Brand 1" not in brands
#         assert "Brand 2" not in brands
#         assert "Brand 3" in brands
    
#     def test_brand_category_list_nonexistent_category(self, api_client):
#         url = reverse("category-brands", kwargs={"category": 999})
#         response = api_client.get(url)
#         assert response.status_code == status.HTTP_200_OK
#         assert len(response.data) == 0

#     def test_brand_category_list_empty_category(self, api_client, category1):
#         url = reverse("category-brands", kwargs={"category": category1.id})
#         response = api_client.get(url)
#         assert response.status_code == status.HTTP_200_OK
#         assert len(response.data) == 0
    
#     def test_brand_category_list_brand_in_multiple_categories(self, api_client, brand1, category1, category2, url_category1, url_category2):
#         brand1.categories.add(category1)
#         brand1.categories.add(category2)

#         response = api_client.get(url_category1)
#         brand_names = [brand["name"] for brand in response.data]
#         assert "Brand 1" in brand_names

#         response = api_client.get(url_category2)
#         brand_names = [brand["name"] for brand in response.data]
#         assert "Brand 1" in brand_names

#     def test_brand_category_list_response_format(self, brand1, category1, api_client, url_category1):
#         brand1.categories.add(category1)
#         response = api_client.get(url_category1)
#         assert response.status_code == status.HTTP_200_OK
#         brand_data = response.data[0]
#         assert "id" in brand_data
#         assert "name" in brand_data

# @pytest.mark.django_db
# class TestCategoryList:
#     def test_category_list_unauthorized_read_access(self, api_client, url_category_list):
#         response = api_client.get(url_category_list)
#         assert response.status_code == status.HTTP_200_OK
    
#     def test_category_list_authorized_read_access(self, api_auth_client, url_category_list):
#         response = api_auth_client.get(url_category_list)
#         assert response.status_code == status.HTTP_200_OK
    
#     def test_category_list_unauthorized_write_access_not_allowed(self, api_client, url_category_list):
#         data = {"name": "New Category", "slug": "new-category"}
        
#         response = api_client.post(url_category_list, data, format="json")
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
#         response = api_client.put(url_category_list, data, format="json")
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
#     def test_category_list_authorized_write_access_not_allowed(self, api_auth_client, url_category_list):
#         data = {"name": "New Category", "slug": "new-category"}
        
#         response = api_auth_client.post(url_category_list, data, format="json")
#         assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        
#         response = api_auth_client.put(url_category_list, data, format="json")
#         assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    
#     def test_category_list_returns_all_categories(self, api_client, category1, category2, category3, url_category_list):
#         response = api_client.get(url_category_list)
#         assert response.status_code == status.HTTP_200_OK
#         assert len(response.data) == 3

#         category_names = [category["name"] for category in response.data]
#         assert "Category 1" in category_names
#         assert "Category 2" in category_names
#         assert "Category 3" in category_names

# @pytest.mark.django_db
# class TestProductViews:
#     def product1_list_pagination(self, api_client, url_product_list):
#         response = api_client.get(url_product_list, {"page": 1, "pageSize": 5})
#         assert response.status_code == status.HTTP_200_OK
#         assert "results" in response.data
#         assert "count" in response.data
    
#     def product1_list_search(self, api_client, url_product_list):
#         response = api_client.get(url_product_list, {"search": "Test"})
#         assert response.status_code == status.HTTP_200_OK
    
#     def product1_category_filter(self, api_client, url_product_category_list):
#         response = api_client.get(url_product_category_list)
#         assert response.status_code == status.HTTP_200_OK
    
#     def product1_price_range_validation(self, api_client, url_product_category_list):
#         with pytest.raises(ValidationError) as context:
#             api_client.get(url_product_category_list, {"price_min": "abc", "price_max": "xyz"})
#         assert "должно быть десятичным числом" in str(context.value)

#         response = api_client.get(url_product_category_list, {"price_min": "10", "price_max": "100"})
#         assert response.status_code == status.HTTP_200_OK
    
#     def product1_brand_filter(self, api_client, brand1, url_product_category_list):
#         response = api_client.get(url_product_category_list, {"selected_brands_ids": brand1.pk})
#         assert response.status_code == status.HTTP_200_OK
    
#     def product1_invalid_brand_ids(self, api_client, url_product_category_list):
#         response = api_client.get(url_product_category_list, {"selected_brands_ids": "a,b,c"})
#         assert response.status_code == status.HTTP_400_BAD_REQUEST
    
#     def product1_ordering(self, api_client, url_product_list):
#         response = api_client.get(url_product_list, {"ordering": "price"})
#         assert response.status_code == status.HTTP_200_OK

#         response = api_client.get(url_product_list, {"ordering": "-price"})
#         assert response.status_code == status.HTTP_200_OK
    
#     def product1_retrieve(self, api_client, product1, url_product_retrieve_change_delete):
#         response = api_client.get(url_product_retrieve_change_delete)
#         assert response.status_code == status.HTTP_200_OK
#         assert response.data["name"] == product1.name
    
#     def product1_update_permissions(self, api_client, url_product_retrieve_change_delete):
#         data = {"name": "Updated Product Name"}
#         response = api_client.patch(url_product_retrieve_change_delete, data, format="json")
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED

# @pytest.mark.django_db
# class TestReviewPagination:
#     def test_pagination_attributes(self):
#         pagination = ReviewPaginationPages()
#         assert pagination.page_query_param == "page"
#         assert pagination.page_size == 10
#         assert pagination.page_size_query_param == "pageSize"
#         assert pagination.max_page_size == 100

# @pytest.mark.django_db
# class TestReviewListCreate:
#     def test_get_reviews_unauthenticated(self, api_client, review1, review2, url_review_list_create):
#         response = api_client.get(url_review_list_create)
#         assert response.status_code == status.HTTP_200_OK
#         assert len(response.data["results"]) == 2
    
#     def test_get_reviews_authenticated(self, api_auth_client, review1, review2, url_review_list_create):
#         response = api_auth_client.get(url_review_list_create)
#         assert response.status_code == status.HTTP_200_OK
#         assert len(response.data["results"]) == 2
    
#     def test_create_review_unauthenticated(self, api_client, product1, url_review_list_create):
#         data = {"product": product1.id, "rating": 4, "title": "Good product", "content": "content1"}
#         response = api_client.post(url_review_list_create, data, format="json")
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
#     def test_create_review_authenticated(self, api_auth_client, product1, url_review_list_create):     
#         data = {"product": product1.id, "rating": 4, "title": "Good product", "content": "content1"}
#         response = api_auth_client.post(url_review_list_create, data, format="json")
#         assert response.status_code == status.HTTP_201_CREATED

#     def test_create_review_authenticated_duplicate(self, api_auth_client, product1, user1, review1, url_review_list_create): 
#         data = {"product": product1.id, "rating": 4, "title": "Good product", "content": "content1"}
#         with pytest.raises(IntegrityError) as context:
#             api_auth_client.post(url_review_list_create, data, format="json")
#         assert "unique constraint" in str(context.value).lower() or \
#                "unique together" in str(context.value).lower()
    
#     def test_create_review_invalid_data(self, api_auth_client, product1, url_review_list_create):
#         data = {"product": product1.id, "rating": 10, "title": "Invalid rating", "content": "content1"}
#         response = api_auth_client.post(url_review_list_create, data, format="json")
#         assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_201_CREATED]

# @pytest.mark.django_db
# class TestReviewRetrieveUpdateDestroy:
#     #retrieve
#     def test_retrieve_review_unauthenticated(self, api_client, review1, url_review_detail):    
#         response = api_client.get(url_review_detail)
        
#         assert response.status_code == status.HTTP_200_OK
#         assert response.data["id"] == review1.id

#     def test_retrieve_review_authenticated_author(self, api_auth_client, review1, url_review_detail):
#         response = api_auth_client.get(url_review_detail)
        
#         assert response.status_code == status.HTTP_200_OK
#         assert response.data["id"] == review1.id
#         assert response.data["title"] == review1.title
#         assert response.data["content"] == review1.content
#         assert response.data["rating"] == review1.rating

#     def test_retrieve_review_authenticated_not_author(self, api_auth_client, user2, product1):
#         user2_review = Review.objects.create(title="Another user review title", content="another user review content", rating=5, product=product1, author=user2)
#         url_user2_review_detail = reverse("product-review", kwargs={"pk": user2_review.pk})
#         response = api_auth_client.get(url_user2_review_detail)

#         assert response.status_code == status.HTTP_200_OK
    
#     def test_retrieve_nonexistent_review(self, api_auth_client):
#         url_nonexistent_review_detail = reverse("product-review", kwargs={"pk": 99999})
#         response = api_auth_client.get(url_nonexistent_review_detail)
        
#         assert response.status_code == status.HTTP_404_NOT_FOUND
    
#     #update
#     def test_update_review_authenticated_author(self, api_auth_client, review1, url_review_detail):
#         data = {"title": "New title", "content": "New content", "rating": 4, "product": review1.product.id}
#         response = api_auth_client.put(url_review_detail, data, format="json")
        
#         assert response.status_code == status.HTTP_200_OK
#         assert response.data["title"] == "New title"
#         assert response.data["content"] == "New content"
#         assert response.data["rating"] == 4
#         review1.refresh_from_db()
#         assert review1.title == "New title"
    
#     def test_partial_update_review_authenticated_author(self, api_auth_client, review1, url_review_detail): 
#         data = {"title": "Частично обновленный"}
#         response = api_auth_client.patch(url_review_detail, data, format="json")
        
#         assert response.status_code == status.HTTP_200_OK
#         assert response.data["title"] == "Частично обновленный"
#         assert response.data["content"] == review1.content
#         review1.refresh_from_db()
#         assert review1.title == "Частично обновленный"

#     def test_update_review_authenticated_not_author(self, api_auth_client, user2, product1):
#         user2_review = Review.objects.create(title="Another user review title", content="Another user review content", rating=5, product=product1, author=user2)
#         url_user2_review = reverse("product-review", kwargs={"pk": user2_review.pk})
#         data = {"title": "Another user review new title", "content": "Another user review new content", "rating": 1, "product": product1.id}
#         response = api_auth_client.put(url_user2_review, data, format="json")
        
#         assert response.status_code == status.HTTP_403_FORBIDDEN
#         user2_review.refresh_from_db()
#         assert user2_review.title == "Another user review title"
#         assert user2_review.content == "Another user review content"
    
#     def test_update_review_unauthenticated(self, api_client, review1, url_review_detail):
#         data = {"title": "Неавторизованное обновление", "content": "Новый контент", "rating": 3, "product": review1.product.id}
#         response = api_client.put(url_review_detail, data, format="json")
        
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED
#         review1.refresh_from_db()
#         assert review1.title != "Неавторизованное обновление"
    
#     #delete
#     def test_delete_review_authenticated_author(self, api_auth_client, review1, url_review_detail):       
#         response = api_auth_client.delete(url_review_detail)
        
#         assert response.status_code == status.HTTP_204_NO_CONTENT
#         assert not Review.objects.filter(pk=review1.pk).exists()
    
#     def test_delete_review_authenticated_not_author(self, api_auth_client, user2, product1):
#         new_review = Review.objects.create(title="Чужой отзыв", content="Контент чужого отзыва", rating=5, product=product1, author=user2)
#         url_user2_review = reverse("product-review", kwargs={"pk": new_review.pk})
#         response = api_auth_client.delete(url_user2_review)
#         assert response.status_code == status.HTTP_403_FORBIDDEN
#         assert Review.objects.filter(pk=new_review.pk).exists()
    
#     def test_delete_review_unauthenticated(self, api_client, review1, url_review_detail):    
#         response = api_client.delete(url_review_detail)
        
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED
#         assert Review.objects.filter(pk=review1.pk).exists()

@pytest.mark.django_db
class TestFavoriteProductViewSet:
    #list
    def test_list_favorites_unauthenticated(self, api_client, url_favorite_product_list_create):
        response = api_client.get(url_favorite_product_list_create)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_favorites_authenticated(self, api_auth_client, favorite_product11, url_favorite_product_list_create):
        response = api_auth_client.get(url_favorite_product_list_create)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["product"]["id"] == favorite_product11.product.id

    #create
    def test_create_favorite_product_unauthenticated(self, api_client, product1, url_favorite_product_list_create):
        response = api_client.post(url_favorite_product_list_create, {"product": product1.id})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_favorite_product_authenticated(self, api_auth_client, product1, url_favorite_product_list_create):
        response = api_auth_client.post(url_favorite_product_list_create, {"product": product1.id})
        assert response.status_code == status.HTTP_201_CREATED
        assert FavoriteProduct.objects.count() == 1
        assert FavoriteProduct.objects.first().user.username == "User1"

    def test_create_favorite_product_duplicate(self, api_auth_client, favorite_product11, url_favorite_product_list_create):
        response = api_auth_client.post(url_favorite_product_list_create, {"product": favorite_product11.product.id})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_favorite_product_nonexistent_product(self, api_auth_client, url_favorite_product_list_create):
        response = api_auth_client.post(url_favorite_product_list_create, {"product": 999})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    #retrieve
    def test_retrieve_favorite_product_unauthorized(self, api_client, favorite_product11, url_favorite_product):
        response = api_client.get(url_favorite_product(favorite_product11.id))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
    def test_retrieve_favorite_product_authenticated(self, api_auth_client, favorite_product11, url_favorite_product):
        response = api_auth_client.get(url_favorite_product(favorite_product11.id))
        assert response.status_code == status.HTTP_200_OK
        assert response.data["product"]["id"] == favorite_product11.product.id

    def test_retrieve_favorite_product_different_user(self, api_auth_client, favorite_product21, url_favorite_product):
        response = api_auth_client.get(url_favorite_product(favorite_product21.id))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_retrieve_nonexistent_favorite_product(self, api_auth_client, url_favorite_product):
        response = api_auth_client.get(url_favorite_product(999))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    #delete
    def test_delete_favorite_product_authenticated(self, api_auth_client, favorite_product11, url_favorite_product):
        response = api_auth_client.delete(url_favorite_product(favorite_product11.id))
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert FavoriteProduct.objects.count() == 0

    def test_delete_favorite_product_different_user(self, api_auth_client, favorite_product11, user2, url_favorite_product):
        favorite_product11.user = user2
        favorite_product11.save()
        response = api_auth_client.delete(url_favorite_product(favorite_product11.id))
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert FavoriteProduct.objects.count() == 1

    #update
    def test_update_favorite_product_not_allowed(self, api_auth_client, favorite_product11, product2, url_favorite_product):
        response = api_auth_client.put(url_favorite_product(favorite_product11.id), {"product": product2.id})
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    #delete_multiple
    def test_delete_multiple_favorite_products_unauthenticated(self, api_client, favorite_product11, favorite_product12, url_favorite_product_delete_multiple):
        response = api_client.delete(url_favorite_product_delete_multiple(favorite_product11.id, favorite_product12.id))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_multiple_favorite_products_success(self, api_auth_client, favorite_product11, favorite_product12, url_favorite_product_delete_multiple):
        assert FavoriteProduct.objects.count() == 2
        response = api_auth_client.delete(url_favorite_product_delete_multiple(favorite_product11.id, favorite_product12.id))
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert FavoriteProduct.objects.count() == 0

    def test_delete_multiple_favorite_products_empty_list(self, api_auth_client, url_favorite_product_delete_multiple):
        response = api_auth_client.delete(url_favorite_product_delete_multiple())
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert FavoriteProduct.objects.count() == 0

    def test_delete_multiple_favorite_products_nonexistent_ids(self, api_auth_client, url_favorite_product_delete_multiple):
        response = api_auth_client.delete(url_favorite_product_delete_multiple(999, 1000))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_multiple_favorite_products_single_id(self, api_auth_client, favorite_product11, favorite_product12, url_favorite_product_delete_multiple):
        assert FavoriteProduct.objects.count() == 2
        response = api_auth_client.delete(url_favorite_product_delete_multiple(favorite_product11.id))
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert FavoriteProduct.objects.count() == 1
        assert FavoriteProduct.objects.first().id == favorite_product12.id

    def test_delete_multiple_different_user_favorites(self, api_auth_client, favorite_product21, favorite_product22, url_favorite_product_delete_multiple):
        response = api_auth_client.delete(url_favorite_product_delete_multiple(favorite_product21.id, favorite_product22.id))
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert FavoriteProduct.objects.count() == 2

# @pytest.mark.django_db
# class TestCartProductListCreate:
#     pass

# @pytest.mark.django_db
# class TestCartProductRetrieveUpdateDestroy:
#     pass

# @pytest.mark.django_db
# class TestCartProductDeleteMultiple:
#     pass