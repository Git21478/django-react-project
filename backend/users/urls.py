from . import views
from django.urls import path, include
from users.views import CreateUserView, PasswordChangeView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    path("user/", views.UserList.as_view(), name="user"),
    path("user/<int:pk>/", views.UserRetrieveUpdate.as_view(), name="user-update"),

    path("profile/", views.ProfileList.as_view(), name="profile"),
    path("profile/<int:pk>/", views.ProfileUpdate.as_view(), name="profile-update"),

    path("user/registration/", CreateUserView.as_view(), name="registration"),
    path("token/", TokenObtainPairView.as_view(), name="get-token"),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("password-change/", PasswordChangeView.as_view(), name="password-change"),

    path("password-reset/", include("django_rest_passwordreset.urls", namespace="password-reset")),

    # path("password-reset/", PasswordResetView.as_view(), name="password-reset"),
    # path("password-reset-done/", PasswordResetDoneView.as_view(), name="password-reset-done"),
    # path("password-reset-confirm/<uidb64>/<token>/", PasswordResetConfirmView.as_view(), name="password-reset-confirm"),
    # path("password-reset-complete/", PasswordResetCompleteView.as_view(), name="password-reset-complete"),
]