from rest_framework import serializers
from .models import Brand, Category, Product, Review, FavoriteProduct, CartProduct

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
        fields = [  "id", "image", "name", "description", "price", "category", "brand", "slug",
                    "rating", "review_amount", "favorite_product_id", "cart_product_id", "is_favorite_product", "is_cart_product" ]
    
    def get_rating(self, obj):
        return obj.get_rating()
    
    def get_review_amount(self, obj):
        return obj.get_review_amount()
    
    def get_favorite_product_id(self, obj):
        return obj.get_favorite_product_id(self.context["request"].user)
    
    def get_cart_product_id(self, obj):
        return obj.get_cart_product_id(self.context["request"].user)
    
    def get_is_favorite_product(self, obj):
        return obj.get_is_favorite_product(self.context["request"].user)
    
    def get_is_cart_product(self, obj):
        return obj.get_is_cart_product(self.context["request"].user)

class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Review
        fields = ["id", "title", "content", "rating", "created_at", "author", "product"]
    
    def validate(self, data):
        if data["rating"] > 5:
            raise serializers.ValidationError("Rating can't be higher than 5")
        return data

class FavoriteProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    
    class Meta:
        model = FavoriteProduct
        fields = ["id", "user", "product"]

class FavoriteProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteProduct
        fields = ["id", "user", "product"]

class CartProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    total_quantity = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartProduct
        fields = ["id", "user", "product", "quantity", "total_quantity", "total_price"]

    def get_total_quantity(self, obj):
        return obj.get_total_quantity(self.context["request"].user)
    
    def get_total_price(self, obj):
        return obj.get_total_price(self.context["request"].user)

class CartProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = ["id", "user", "product", "quantity"]