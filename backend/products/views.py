import uuid

from django.core.cache import cache
from django.db import transaction
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import (
    AnonymousCart,
    AnonymousFavorite,
    Brand,
    Cart,
    CartProduct,
    Category,
    Favorite,
    Product,
    Review,
)
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    AddToCartSerializer,
    AnonymousCartSerializer,
    AnonymousFavoriteSerializer,
    BrandSerializer,
    CartProductSerializer,
    CartSerializer,
    CategorySerializer,
    FavoriteCreateSerializer,
    FavoriteSerializer,
    ProductSerializer,
    ReviewSerializer,
)


# Brand
@extend_schema(tags=["Бренды"])
class BrandCategoryList(generics.ListAPIView):
    serializer_class = BrandSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Brand.objects.filter(
            categories__id=self.kwargs["category"]
        ).prefetch_related("categories")


# Category
CATEGORY_CACHE_KEY = "categories:all:v1"
CATEGORY_CACHE_TTL = 60 * 60


@extend_schema(tags=["Категории"])
class CategoryList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        data = cache.get(CATEGORY_CACHE_KEY)
        if data is None:
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            data = serializer.data
            cache.set(CATEGORY_CACHE_KEY, data, CATEGORY_CACHE_TTL)
        return Response(data)


# Product
class ProductPaginationPages(PageNumberPagination):
    page_query_param = "page"
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


@extend_schema(tags=["Товары"])
class ProductList(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    pagination_class = ProductPaginationPages
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name", "description"]
    ordering_fields = ["price", "rating"]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def get_queryset(self):
        queryset = (
            Product.objects.select_related("category", "brand")
            .prefetch_related("reviews")
            .order_by("id")
        )
        params = self.request.query_params

        category_id = params.get("category_id")
        if category_id not in (None, ""):
            queryset = queryset.filter(category_id=category_id)

        price_min = params.get("price_min") 
        if price_min not in (None, ""):
            queryset = queryset.filter(price__gte=price_min)

        price_max = params.get("price_max")
        if price_max not in (None, ""):
            queryset = queryset.filter(price__lte=price_max)

        brand_ids = params.get("brand_ids")
        if brand_ids:
            brand_ids = [i for i in brand_ids.split(",")]
            queryset = queryset.filter(brand_id__in=brand_ids)

        return queryset


@extend_schema(tags=["Товары"])
class ProductRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Product.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


# Review
class ReviewPaginationPages(PageNumberPagination):
    page_query_param = "page"
    page_size = 10
    page_size_query_param = "pageSize"
    max_page_size = 100


@extend_schema(tags=["Отзывы"])
class ReviewListCreate(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    pagination_class = ReviewPaginationPages
    filter_backends = [OrderingFilter]
    ordering_fields = ["created_at", "rating"]
    ordering = ["-created_at", "id"]

    def get_queryset(self):
        return Review.objects.select_related("author").filter(
            product=self.kwargs.get("product_id"),
        )

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            product_id=self.kwargs.get("product_id"),
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        product_id = self.kwargs.get("product_id")
        reviews = Review.objects.filter(product_id=product_id)
        response_serializer = self.get_serializer(reviews, many=True)

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Отзывы"])
class ReviewRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def delete(self, request, *args, **kwargs):
        review = get_object_or_404(Review, pk=self.kwargs.get("pk"))
        product_id = review.product.id
        review.delete()

        reviews = Review.objects.filter(product_id=product_id)
        response_serializer = self.get_serializer(reviews, many=True)

        return Response(response_serializer.data, status=status.HTTP_200_OK)


# Favorite
@extend_schema(tags=["Избранные товары"])
class FavoriteViewSet(ModelViewSet):
    permission_classes = [AllowAny]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Favorite.objects.filter(user=self.request.user)

        session_key = self.request.headers.get("X-Session-Key")
        if session_key:
            return AnonymousFavorite.objects.filter(session_key=session_key)

        return AnonymousFavorite.objects.none()

    def get_serializer_class(self):
        if self.action == "create":
            return FavoriteCreateSerializer
        elif self.request.user.is_authenticated:
            return FavoriteSerializer
        else:
            return AnonymousFavoriteSerializer

    def get_serializer_context(self):
        return {"request": self.request}

    def perform_create(self, serializer):
        request = self.request

        if request.user.is_authenticated:
            serializer.save(user=request.user)
        else:
            if not request.headers.get("X-Session-Key"):
                request.session.save()
            serializer.save(session_key=request.headers.get("X-Session-Key"))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        return Response(
            {"error": "Метод PUT не разрешён"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def partial_update(self, request, *args, **kwargs):
        return Response(
            {"error": "Метод PATCH не разрешён"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    @action(detail=False, methods=["delete"], url_path="delete-multiple")
    def delete_multiple(self, request):
        ids_param = request.query_params.get("ids", "")

        if not ids_param:
            return Response(
                {"error": "Не указаны ID для удаления"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            selected_ids = [int(id.strip()) for id in ids_param.split(",")]
        except ValueError:
            return Response(
                {"error": "Некорректный формат ID"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_favorites = self.get_queryset().filter(id__in=selected_ids)
        deleted_count, _ = user_favorites.delete()

        if deleted_count == 0:
            return Response(
                {"error": "Избранные товары не найдены"},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            {"message": f"Товаров удалено: {deleted_count}"},
            status=status.HTTP_204_NO_CONTENT,
        )

    @action(detail=False, methods=["post"], url_path="migrate")
    def migrate_to_user(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"error": "Необходима аутентификация"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        session_key = request.headers.get("X-Session-Key")
        if not session_key:
            return Response(
                {"message": "Нет анонимного пользователя для переноса"},
                status=status.HTTP_200_OK,
            )

        anonymous_favorites = AnonymousFavorite.objects.filter(
            session_key=session_key
        ).only("product_id")
        if not anonymous_favorites.exists():
            return Response(
                {"message": "Нет избранного для переноса"},
                status=status.HTTP_200_OK,
            )

        with transaction.atomic():
            for favorite in anonymous_favorites:
                Favorite.objects.get_or_create(
                    user=request.user,
                    product_id=favorite.product_id,
                )
            AnonymousFavorite.objects.filter(session_key=session_key).delete()

        return Response(status=status.HTTP_200_OK)


# Cart
@extend_schema(tags=["Корзины"])
class CartViewSet(ModelViewSet):
    permission_classes = [AllowAny]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Cart.objects.filter(user=self.request.user)

        session_key = self.request.headers.get("X-Session-Key")
        if session_key:
            return AnonymousCart.objects.filter(session_key=session_key)
        else:
            return AnonymousCart.objects.none()

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            return CartSerializer
        else:
            return AnonymousCartSerializer

    def get_object(self):
        if self.request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=self.request.user)
            return cart

        session_key = self.request.headers.get("X-Session-Key")

        if not session_key:
            session_key = str(uuid.uuid4())

        cart, created = AnonymousCart.objects.get_or_create(session_key=session_key)
        return cart

    def list(self, request, *args, **kwargs):
        cart = self.get_object()
        serializer = self.get_serializer(cart, context={"request": request})
        return Response(serializer.data)

    @action(detail=False, methods=["post"], url_path="add")
    def add_product(self, request):
        cart = self.get_object()
        serializer = AddToCartSerializer(
            data=request.data,
            context={"request": request},
        )

        if serializer.is_valid():
            product = serializer.validated_data.get("product")
            quantity = serializer.validated_data.get("quantity", 1)

            if request.user.is_authenticated:
                cart_product, created = CartProduct.objects.get_or_create(
                    cart=cart,
                    product=product,
                    defaults={"quantity": quantity},
                )
            else:
                cart_product, created = CartProduct.objects.get_or_create(
                    anonymous_cart=cart,
                    product=product,
                    defaults={"quantity": quantity},
                )

            if not created:
                cart_product.quantity += quantity
                cart_product.save()

            return Response(
                CartProductSerializer(cart_product, context={"request": request}).data,
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["patch"], url_path="update/(?P<product_id>\\d+)")
    def update_product(self, request, product_id=None):
        cart = self.get_object()

        if request.user.is_authenticated:
            cart_product = get_object_or_404(
                CartProduct,
                cart=cart,
                product_id=product_id,
            )
        else:
            cart_product = get_object_or_404(
                CartProduct,
                anonymous_cart=cart,
                product_id=product_id,
            )

        quantity = request.data.get("quantity")
        if quantity is not None and int(quantity) > 0:
            cart_product.quantity = quantity
            cart_product.save()
        else:
            return Response(
                {"quantity": "Количество товара должно быть положительным числом"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cart_serializer = self.get_serializer(cart, context={"request": request})
        return Response(cart_serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["delete"], url_path="remove/(?P<product_id>\\d+)")
    def remove_product(self, request, product_id=None):
        cart = self.get_object()

        if request.user.is_authenticated:
            cart_product = get_object_or_404(
                CartProduct,
                cart=cart,
                product_id=product_id,
            )
        else:
            cart_product = get_object_or_404(
                CartProduct,
                anonymous_cart=cart,
                product_id=product_id,
            )

        cart_product.delete()

        serializer = self.get_serializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["delete"], url_path="delete-multiple")
    def delete_multiple(self, request):
        cart_product_ids = request.data.get("cart_product_ids", [])
        cart = self.get_object()

        if request.user.is_authenticated:
            CartProduct.objects.filter(
                cart=cart,
                id__in=cart_product_ids,
            ).delete()
        else:
            CartProduct.objects.filter(
                anonymous_cart=cart,
                id__in=cart_product_ids,
            ).delete()

        serializer = self.get_serializer(cart, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["delete"], url_path="clear")
    def clear_cart(self, request):
        cart = self.get_object()

        if request.user.is_authenticated:
            CartProduct.objects.filter(cart=cart).delete()
        else:
            CartProduct.objects.filter(anonymous_cart=cart).delete()

        serializer = self.get_serializer(cart, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
