from .models import Brand, Category, Product, Review, FavoriteProduct, CartProduct
from .serializers import BrandSerializer, CategorySerializer, ProductSerializer, ReviewSerializer, FavoriteProductSerializer, FavoriteProductCreateSerializer, CartProductSerializer, CartProductCreateSerializer
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError as DRFValidationError
from django.db.models import Avg
from .permissions import IsAuthorOrReadOnly

#Brand
class BrandCategoryList(generics.ListAPIView):
    serializer_class = BrandSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Brand.objects.filter(categories__id=self.kwargs["category"])

#Category
class CategoryList(generics.ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Category.objects.all()

#Product
class ProductPaginationPages(PageNumberPagination):
    page_query_param = "page"
    page_size = 10
    page_size_query_param = 'pageSize'
    max_page_size = 100

class BaseProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny] # AllowAny / IsAdmin

    pagination_class = ProductPaginationPages
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name", "description"]
    ordering_fields = ["price", "rating"]

class ProductList(BaseProductListView):
    def get_queryset(self):
        return Product.objects.annotate(rating=Avg("reviews__rating")).select_related("brand", "category").order_by("id")

class ProductCategoryList(BaseProductListView):
    def get_queryset(self):
        price_min = self.request.query_params.get("price_min", 0)
        price_max = self.request.query_params.get("price_max", 1000000000)
        selected_brands_ids = self.request.query_params.get("selected_brands_ids")

        if selected_brands_ids:
            try:
                selected_brands_ids = [int(i) for i in selected_brands_ids.split(",")]
                return Product.objects.filter(category=self.kwargs["pk"], price__range=(price_min, price_max), brand__in=selected_brands_ids).order_by("id")
            except (ValueError, AttributeError):
                raise DRFValidationError("Некорректные данные")
        return Product.objects.filter(category=self.kwargs["pk"], price__range=(price_min, price_max)).order_by("id")

class ProductRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Product.objects.all()

#Review
class ReviewPaginationPages(PageNumberPagination):
    page_query_param = "page"
    page_size = 10
    page_size_query_param = 'pageSize'
    max_page_size = 100

class ReviewListCreate(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    pagination_class = ReviewPaginationPages
    filter_backends = [OrderingFilter]
    ordering_fields = ["created_at", "rating"]
    ordering = ["-created_at", "id"]

    def get_queryset(self):
        return Review.objects.select_related("author").filter(product=self.kwargs["product_id"])
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class ReviewRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrReadOnly]

#Favorites
class FavoriteProductListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FavoriteProduct.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return FavoriteProductCreateSerializer
        else:
            return FavoriteProductSerializer
    
    def get_serializer_context(self):
        return {"request": self.request}
    
    def perform_create(self, serializer):    
        serializer.save(user=self.request.user)

class FavoriteProductRetrieveDestroy(generics.RetrieveDestroyAPIView):
    serializer_class = FavoriteProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FavoriteProduct.objects.filter(user=self.request.user)
    
    def get_serializer_context(self):
        return {"request": self.request}

class FavoriteProductDeleteMultiple(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, *args, **kwargs):
        ids_param = request.query_params.get('ids', '')
        if not ids_param:
            return Response({"error": "Не указаны ID для удаления"}, status=status.HTTP_400_BAD_REQUEST)
        selected_ids = [int(id.strip()) for id in ids_param.split(',')]
        
        user_favorite_products = FavoriteProduct.objects.filter(id__in=selected_ids, user=request.user)
        
        deleted_count, _ = user_favorite_products.delete()
        if deleted_count == 0:
            return Response({"error": "Избранные товары не найдены"}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(status=status.HTTP_204_NO_CONTENT)

#Cart
class CartProductListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartProduct.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return CartProductCreateSerializer
        else:
            return CartProductSerializer
    
    def get_serializer_context(self):
        return {"request": self.request}
    
    def get(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        total_quantity = response.data[0]["total_quantity"] if len(response.data) > 0 else 0
        total_price = response.data[0]["total_price"] if len(response.data) > 0 else 0
        response.data = {"cart_products": response.data, "total_quantity": total_quantity, "total_price": total_price}
        return response
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CartProductRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartProduct.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        return {"request": self.request}

class CartProductDeleteMultiple(generics.ListAPIView):
    serializer_class = CartProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartProduct.objects.filter(user=self.request.user)
    
    def update(self, request, *args, **kwargs):
        selected_ids = self.request.data.get("cartProductsIds")
        selected_objects = CartProduct.objects.filter(id__in=selected_ids)
        if len(selected_objects) > 0:
            selected_objects.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_200_OK)