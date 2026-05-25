from . import views
from django.urls import path, include
from users.views import CreateUserView, PasswordChangeView
from rest_framework_simplejwt.views import TokenRefreshView
from .views import CustomTokenObtainPairView

urlpatterns = [
    path("user/", views.UserList.as_view(), name="user"),
    path("user/<int:pk>/", views.UserRetrieveUpdate.as_view(), name="user-update"),

    path("profile/", views.ProfileList.as_view(), name="profile"),
    path("profile/<int:pk>/", views.ProfileUpdate.as_view(), name="profile-update"),

    path("user/registration/", CreateUserView.as_view(), name="registration"),
    path("token/", CustomTokenObtainPairView.as_view(), name="get-token"),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("password-change/", PasswordChangeView.as_view(), name="password-change"),

    path("password-reset/", include("django_rest_passwordreset.urls", namespace="password-reset")),
]