from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"favorite-products", views.FavoriteProductViewSet, basename="favorite-product")
router.register(r"cart-products", views.CartProductViewSet, basename="cart-product")

urlpatterns = [
    path("categories/<int:category>/brands/", views.BrandCategoryList.as_view(), name="category-brands"),

    path("categories/", views.CategoryList.as_view(), name="category-list"),

    path("products/", views.ProductList.as_view(), name="product-list"),
    path("catalog/<int:pk>/products/", views.ProductCategoryList.as_view(), name="product-category-list"),
    path("products/<int:pk>/", views.ProductRetrieveUpdateDestroy.as_view(), name="product-retrieve-change-delete"),

    path("products/<int:product_id>/reviews/", views.ReviewListCreate.as_view(), name="product-review-list-create"),
    path("products/reviews/<int:pk>/", views.ReviewRetrieveUpdateDestroy.as_view(), name="product-review"),

    path("", include(router.urls)),
]