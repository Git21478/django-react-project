from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers

from .models import (
    Brand,
    Cart,
    CartProduct,
    Category,
    Favorite,
    Product,
    Review,
)


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "name", "categories"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "brands"]


class ProductSerializer(serializers.ModelSerializer):
    favorite_id = serializers.SerializerMethodField()
    cart_product_id = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()
    is_cart_product = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "image",
            "name",
            "description",
            "price",
            "category",
            "brand",
            "slug",
            "rating",
            "review_count",
            "favorite_id",
            "cart_product_id",
            "is_favorite",
            "is_cart_product",
        ]

    def get_favorite_id(self, obj):
        request = self.context.get("request")
        return obj.get_favorite_id(request) if request else None

    def get_cart_product_id(self, obj):
        request = self.context.get("request")
        return obj.get_cart_product_id(request) if request else None

    def get_is_favorite(self, obj):
        request = self.context.get("request")
        return obj.get_is_favorite(request) if request else False

    def get_is_cart_product(self, obj):
        request = self.context.get("request")
        return obj.get_is_cart_product(request) if request else False


class ReviewSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(
        validators=[
            MinValueValidator(1, "Рейтинг не может быть меньше 1"),
            MaxValueValidator(5, "Рейтинг не может быть больше 5"),
        ]
    )
    author_id = serializers.IntegerField(source="author.id", read_only=True)
    author = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "title",
            "content",
            "rating",
            "created_at",
            "author_id",
            "author",
            "product_id",
        ]


# Favorite
class FavoriteSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ["id", "product", "created_at"]


class FavoriteCreateSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source="product", write_only=True
    )

    class Meta:
        model = Favorite
        fields = ["id", "product", "product_id"]
        read_only_fields = ["product"]

    def to_representation(self, instance):
        return FavoriteSerializer(instance, context=self.context).data

    def validate(self, data):
        request = self.context.get("request")
        if not request:
            raise serializers.ValidationError("Request не найден")

        product = data.get("product")

        if request.user.is_authenticated:
            if Favorite.objects.filter(product=product, user=request.user).exists():
                raise serializers.ValidationError(
                    {"product": "Этот товар уже добавлен в избранное"}
                )
            return data

        session_key = request.session.session_key
        if (
            session_key
            and Favorite.objects.filter(
                product=product, session_key=session_key, user__isnull=True
            ).exists()
        ):
            raise serializers.ValidationError(
                {"product": "Этот товар уже добавлен в избранное"}
            )

        return data


# Cart
class CartProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = CartProduct
        fields = ["id", "product", "quantity", "total_price"]


class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(write_only=True, min_value=1)
    quantity = serializers.IntegerField(write_only=True, min_value=1, default=1)

    def validate(self, data):
        request = self.context.get("request")
        if not request:
            raise serializers.ValidationError("Контекст запроса (request) не найден.")

        try:
            product = Product.objects.get(id=data.get("product_id"))
        except Product.DoesNotExist:
            raise serializers.ValidationError({"product_id": "Товар не найден"})

        if request.user.is_authenticated:
            if CartProduct.objects.filter(
                product=product, cart__user=request.user
            ).exists():
                raise serializers.ValidationError(
                    {"product_id": "Этот товар уже есть в корзине"}
                )

        else:
            session_key = request.session.session_key
            if (
                session_key
                and CartProduct.objects.filter(
                    product=product,
                    cart__session_key=session_key,
                    cart__user__isnull=True,
                ).exists()
            ):
                raise serializers.ValidationError(
                    {"product_id": "Этот товар уже есть в корзине"}
                )

        data["product"] = product
        return data


class CartSerializer(serializers.ModelSerializer):
    cart_products = CartProductSerializer(source="products", many=True, readonly=True)
    total_quantity = serializers.ReadOnlyField()
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = Cart
        fields = [
            "id",
            "cart_products",
            "total_quantity",
            "total_price",
            "created_at",
            "updated_at",
        ]
