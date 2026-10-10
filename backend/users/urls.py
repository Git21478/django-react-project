from django.urls import path

from users.views import CreateUserView, LoginView, LogoutView, PasswordChangeView

from . import views
from .views import (
    CustomResetPasswordConfirm,
    CustomResetPasswordRequestToken,
    CustomResetPasswordValidateToken,
    S3FileView,
)

urlpatterns = [
    path("user/", views.UserList.as_view(), name="user"),
    path("user/<int:pk>/", views.UserRetrieveUpdate.as_view(), name="user-update"),
    path("profile/", views.ProfileList.as_view(), name="profile"),
    path("profile/<int:pk>/", views.ProfileUpdate.as_view(), name="profile-update"),
    path("registration/", CreateUserView.as_view(), name="registration"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("password-change/", PasswordChangeView.as_view(), name="password-change"),
    path(
        "password-reset/",
        CustomResetPasswordRequestToken.as_view(),
        name="password-reset-request",
    ),
    path(
        "password-reset/confirm/",
        CustomResetPasswordConfirm.as_view(),
        name="password-reset-confirm",
    ),
    path(
        "password-reset/validate_token/",
        CustomResetPasswordValidateToken.as_view(),
        name="password-reset-validate",
    ),
    path("files/<path:file_path>", S3FileView.as_view(), name="s3-file"),
]
