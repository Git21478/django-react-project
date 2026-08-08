from rest_framework import serializers
from .models import User, Profile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .utils import merge_favorites, merge_carts


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    # def validate(self, data):
    #     if data["password"] == "asd":
    #         raise serializers.ValidationError("Password should not be 'asd'")
    #     return data


class PasswordChangeSerializer(serializers.Serializer):
    model = User

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        request = self.context.get("request")
        session_key = request.headers.get("X-Session-Key") if request else None

        if session_key and session_key.strip():
            cart_merged = merge_carts(self.user, session_key)
            if cart_merged:
                data["cart_merged"] = True

            favorites_merged = merge_favorites(self.user, session_key)
            if favorites_merged:
                data["favorites_merged"] = True

        return data


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["user", "avatar", "phone", "city"]
