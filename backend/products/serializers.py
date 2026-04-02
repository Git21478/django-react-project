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
    favorite_product_id = serializers.SerializerMethodField()
    cart_product_id = serializers.SerializerMethodField()
    is_favorite_product = serializers.SerializerMethodField()
    is_cart_product = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id", "image", "name", "description", "price",
            "category", "brand", "slug", "rating", "review_amount",
            "favorite_product_id", "cart_product_id", "is_favorite_product", "is_cart_product"
        ]
    
    def get_rating(self, obj):
        return obj.get_rating()
    
    def get_review_amount(self, obj):
        return obj.get_review_amount()
    
    def get_favorite_product_id(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.get_favorite_product_id(request.user)

        session_key = request.session.session_key if request else None
        if session_key:
            favorite_product = AnonymousFavorite.objects.filter(
                session_key = session_key,
                product = obj
            ).first()
            return favorite_product.id if favorite_product else None
        return None
    
    def get_cart_product_id(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.get_cart_product_id(request.user)
        
        session_key = request.session.session_key if request else None
        if session_key:
            cart_product = CartProduct.objects.filter(
                anonymous_cart__session_key = session_key,
                product = obj
            ).first()
            return cart_product.id if cart_product else None
        return None
    
    def get_is_favorite_product(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.get_is_favorite_product(request.user)

        session_key = request.session.session_key if request else None
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
        
        session_key = request.session.session_key if request else None
        if session_key:
            return CartProduct.objects.filter(
                anonymous_cart__session_key = session_key,
                product = obj
            ).exists()
        return False

class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Review
        fields = ["id", "title", "content", "rating", "created_at", "author", "product"]
    
    def validate_rating(self, data):
        rating = data.get("rating")
        if rating is not None:
            if rating > 5:
                raise serializers.ValidationError("Rating can't be higher than 5")
            if rating < 1:
                raise serializers.ValidationError("Rating can't be lower than 1")
        return data

#Favorites
class FavoriteSerializer(serializers.ModelSerializer): #? user
    product = ProductSerializer(read_only=True)
    
    class Meta:
        model = Favorites
        fields = ["id", "product", "created_at"]

class AnonymousFavoriteSerializer(serializers.ModelSerializer): #? session
    product = ProductSerializer(read_only=True)
    
    class Meta:
        model = AnonymousFavorite
        fields = ["id", "product", "created_at"]

class FavoriteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ["id", "product"]
    
    def validate(self, data):
        request = self.context.get("request")
        product = data.get("product")

        if not request:
            raise serializers.ValidationError("Request не найден")

        elif request.user.is_authenticated:
            if Favorite.objects.filter(product=product, user=request.user).exists():
                raise serializers.ValidationError({"product": "Этот товар уже добавлен в избранное"})
        else:
            if not request.session.session_key:
                request.session.save()

            if AnonymousFavorite.objects.filter(product=product, session_key=request.session.session_key).exists():
                raise serializers.ValidationError({"product": "Этот товар уже добавлен в избранное"})

        return data
    
    def create(self, validated_data):
        request = self.context.get("request")
        product = validated_data.get("product")

        if request.user.is_authenticated:
            return Favorite.objects.create(user=request.user, product=product)
        
        else:
            if not request.session.session_key:
                request.session.save()

            return Favorite.objects.create(session_key=request.session.session_key, product=product)  

#Cart 
class BaseCartSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    total_quantity = serializers.IntegerField(read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        abstract = True
        fields = ["id", "products", "total_quantity", "total_price", "created_at", "updated_at"]
    
    def get_products(self, obj):
        from .serializers import CartProductSerializer
        products = obj.products.all()
        return CartProductSerializer(products, many=True, context=self.context).data

class CartSerializer(BaseCartSerializer):
    class Meta:
        model = Cart

class AnonymousCartSerializer(BaseCartSerializer):
    class Meta:
        model = AnonymousCart

class CartProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source="product", write_only=True)

    class Meta:
        model = CartProduct
        fields = ["id", "product", "product_id", "quantity", "total_price", "created_at"]

class CartProductCreateSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source="product", write_only=True)

    class Meta:
        model = CartProduct
        fields = ["id", "product_id", "quantity"]

    def validate(self, data):
        request = self.context.get("request")
        product = data.get("product")

        if request and request.user.is_authenticated:
            if CartProduct.objects.filter(product=product, cart__user=request.user).exists():
                raise serializers.ValidationError({"product_id": "Этот товар уже добавлен в корзину"})
        return data