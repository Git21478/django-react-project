from rest_framework import serializers
from .models import (
    Brand, Category, Product, Review, 
    Favorite, AnonymousFavorite, Cart, AnonymousCart, CartProduct
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
    rating = serializers.SerializerMethodField()
    review_amount = serializers.SerializerMethodField()
    favorite_id = serializers.SerializerMethodField()
    cart_product_id = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()
    is_cart_product = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id", "image", "name", "description", "price",
            "category", "brand", "slug", "rating", "review_amount",
            "favorite_id", "cart_product_id", "is_favorite", "is_cart_product"
        ]
    
    def get_rating(self, obj):
        return obj.get_rating()
    
    def get_review_amount(self, obj):
        return obj.get_review_amount()
    
    def get_favorite_id(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.get_favorite_id(request.user)

        session_key = request.headers.get("X-Session-Key") if request else None
        if session_key:
            favorite = AnonymousFavorite.objects.filter(
                session_key = session_key,
                product = obj
            ).first()
            return favorite.id if favorite else None
        return None
    
    def get_cart_product_id(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.get_cart_product_id(request.user)
        
        session_key = request.headers.get("X-Session-Key") if request else None
        if session_key:
            cart_product = CartProduct.objects.filter(
                anonymous_cart__session_key = session_key,
                product = obj
            ).first()
            return cart_product.id if cart_product else None
        return None
    
    def get_is_favorite(self, obj):
        request = self.context.get("request")

        if request and request.user.is_authenticated:
            exists = obj.get_is_favorite(request.user)
            return exists

        session_key = request.headers.get("X-Session-Key") if request else None
        if session_key:
            return AnonymousFavorite.objects.filter(
                session_key = session_key,
                product = obj
            ).exists()
        return False
    
    def get_is_cart_product(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.get_is_cart_product(request.user)
        
        session_key = request.headers.get("X-Session-Key") if request else None
        if session_key:
            return CartProduct.objects.filter(
                anonymous_cart__session_key = session_key,
                product = obj
            ).exists()
        return False

class ReviewSerializer(serializers.ModelSerializer):
    author_id = serializers.IntegerField(source="author.id", read_only=True)
    author = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Review
        fields = ["id", "title", "content", "rating", "created_at", "author_id", "author", "product_id"]
    
    def validate_rating(self, rating):
        if rating is not None:
            if rating > 5:
                raise serializers.ValidationError("Rating can't be higher than 5")
            if rating < 1:
                raise serializers.ValidationError("Rating can't be lower than 1")
        return rating

#Favorite
class FavoriteSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    
    class Meta:
        model = Favorite
        fields = ["id", "product", "created_at"]

class AnonymousFavoriteSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    
    class Meta:
        model = AnonymousFavorite
        fields = ["id", "product", "created_at"]

class FavoriteCreateSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source="product", write_only=True)

    class Meta:
        model = Favorite
        fields = ["id", "product", "product_id"]
        read_only_fields = ["product"]

    def to_representation(self, instance):
        return FavoriteSerializer(instance, context=self.context).data
    
    def validate(self, data):
        request = self.context.get("request")
        product = data.get("product")

        if not request:
            raise serializers.ValidationError("Request не найден")

        elif request.user.is_authenticated:
            if Favorite.objects.filter(product=product, user=request.user).exists():
                raise serializers.ValidationError({"product": "Этот товар уже добавлен в избранное"})
        else:
            if request.headers.get("X-Session-Key"):
                if AnonymousFavorite.objects.filter(product=product, session_key=request.headers.get("X-Session-Key")).exists():
                    raise serializers.ValidationError({"product": "Этот товар уже добавлен в избранное"})

        return data
    
    def create(self, validated_data):
        request = self.context.get("request")
        product = validated_data.get("product")

        if request.user.is_authenticated:
            favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
            return favorite
        
        else:
            if not request.headers.get("X-Session-Key"):
                self.request.session.create()

            favorite, created = AnonymousFavorite.objects.get_or_create(session_key=request.headers.get("X-Session-Key"), product=product)
            return favorite

#Cart 
class CartProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartProduct
        fields = ["id", "product", "quantity", "total_price"]
    
    def get_total_price(self, obj):
        return obj.total_price

class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(write_only=True, min_value=1)
    quantity = serializers.IntegerField(write_only=True, min_value=1, default=1)
    
    def validate_product_id(self, value):
        try:
            return value
        except Product.DoesNotExist:
            raise serializers.ValidationError("Товар не найден")

    def validate(self, data):
        request = self.context.get("request")
        product = Product.objects.get(id=data.get("product_id")) 
        
        if not request or not product:
            return data

        if request.user.is_authenticated:
            if CartProduct.objects.filter(product=product, cart__user=request.user).exists():
                raise serializers.ValidationError({"product_id": "Этот товар уже есть в корзине"})
        
        data["product"] = product
        return data
        
class BaseCartSerializer(serializers.ModelSerializer):
    cart_products = serializers.SerializerMethodField()
    total_quantity = serializers.IntegerField(read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        abstract = True
        fields = ["id", "cart_products", "total_quantity", "total_price", "created_at", "updated_at"]
    
    def get_cart_products(self, obj):
        from .serializers import CartProductSerializer
        products = obj.products.all()
        return CartProductSerializer(products, many=True, context=self.context).data

class CartSerializer(BaseCartSerializer):
    class Meta:
        model = Cart
        fields = BaseCartSerializer.Meta.fields

class AnonymousCartSerializer(BaseCartSerializer):
    class Meta:
        model = AnonymousCart
        fields = BaseCartSerializer.Meta.fields