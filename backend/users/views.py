from urllib.parse import urlparse

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseForbidden
from django_rest_passwordreset.views import (
    ResetPasswordConfirm,
    ResetPasswordRequestToken,
    ResetPasswordValidateToken,
)
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import generics, serializers, status
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from storages.backends.s3boto3 import S3Boto3Storage

from .models import Profile, User
from .serializers import (
    LoginSerializer,
    PasswordChangeSerializer,
    ProfileSerializer,
    UserSerializer,
)


# User
@extend_schema(tags=["Пользователи"])
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


@extend_schema(tags=["Пользователи"])
class UserList(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)
    

@extend_schema(tags=["Пользователи"])
class UserRetrieveUpdate(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


# Profile
@extend_schema(tags=["Профили пользователей"])
class ProfileList(generics.ListCreateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user.id)


@extend_schema(tags=["Профили пользователей"])
class ProfileUpdate(generics.UpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.all()
    

# Auth
@extend_schema(tags=["Аутентификация"])
class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = authenticate(request, username=email, password=password)
        if user is None:
            return Response(
                {"detail": "Неверный email или пароль"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        login(request, user)
        return Response({"detail": "OK"}, status=status.HTTP_200_OK)


@extend_schema(tags=["Аутентификация"])
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"detail": "OK"})

    
@extend_schema(tags=["Аутентификация"])
class PasswordChangeView(generics.UpdateAPIView):
    serializer_class = PasswordChangeSerializer
    model = User
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Password updated succesfully",
                "data": [],
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["Аутентификация"],
    request=inline_serializer(
        name="PasswordResetRequest",
        fields={"email": serializers.EmailField()},
    ),
    responses={200: inline_serializer(
        name="PasswordResetResponse",
        fields={"status": serializers.CharField()},
    )},
)
class CustomResetPasswordRequestToken(ResetPasswordRequestToken):
    pass

@extend_schema(
    tags=["Аутентификация"],
    request=inline_serializer(
        name="PasswordResetConfirm",
        fields={
            "password": serializers.CharField(),
            "token": serializers.CharField(),
        },
    ),
    responses={200: None},
)
class CustomResetPasswordConfirm(ResetPasswordConfirm):
    pass

@extend_schema(
    tags=["Аутентификация"],
    request=inline_serializer(
        name="PasswordResetValidateToken",
        fields={"token": serializers.CharField()},
    ),
    responses={200: inline_serializer(
        name="PasswordResetValidateTokenResponse",
        fields={"status": serializers.CharField()},
    )},
)
class CustomResetPasswordValidateToken(ResetPasswordValidateToken):
    pass


# S3
@extend_schema(tags=["Файлы"])
class S3FileView(APIView):
    def get(self, request, file_path):
        if not file_path.startswith(("product_images/", "profile_avatars/")):
            return HttpResponseForbidden()

        client = S3Boto3Storage().connection.meta.client
        url = client.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": settings.AWS_STORAGE_BUCKET_NAME,
                "Key": file_path,
            },
            ExpiresIn=settings.AWS_S3_URL_EXPIRATION,
        )

        parsed = urlparse(url)
        internal_path = parsed.path + "?" + parsed.query

        response = HttpResponse()
        response["X-Accel-Redirect"] = f"/internal-s3{internal_path}"
        return response