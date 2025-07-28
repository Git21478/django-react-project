from django.urls import path
from . import views

urlpatterns = [
    path("categories/<int:category>/brands/", views.BrandCategoryList.as_view(), name="category-brands"),

    path("categories/", views.CategoryList.as_view(), name="category-list"),

    path("products/", views.ProductList.as_view(), name="product-list"),
    path("catalog/<slug:category_slug>/products/", views.ProductCategoryList.as_view(), name="product-list"),
    path("products/<int:pk>/", views.ProductRetrieveUpdateDestroy.as_view(), name="product-retrieve-change-delete"),

    path("products/<int:product_id>/reviews/", views.ReviewListCreate.as_view(), name="product-review-list"),
    path("products/reviews/<int:pk>/", views.ReviewRetrieveUpdateDestroy.as_view(), name="product-review"),

    path("favorite-products/", views.FavoriteProductListCreate.as_view(), name="favorite-product-list-create"),
    path("favorite-products/<int:pk>/", views.FavoriteProductRetrieveUpdateDestroy.as_view(), name="favorite-product"),
    path("favorite-products/delete-multiple/", views.FavoriteProductDeleteMultiple.as_view(), name="favorite-product-delete-multiple"),

    path("cart-products/", views.CartProductListCreate.as_view(), name="cart-product-list-create"),
    path("cart-products/<int:pk>/", views.CartProductRetrieveUpdateDestroy.as_view(), name="cart-product"),
    path("cart-products/delete-multiple/", views.CartProductDeleteMultiple.as_view(), name="cart-product-delete-multiple"),
]