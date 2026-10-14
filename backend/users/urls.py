from django.urls import path

from . import views

urlpatterns = [
    path("registration/", views.RegisterView.as_view(), name="registration"),
    path("user/me/", views.CurrentUserView.as_view(), name="current-user"),
    path("profile/me/", views.CurrentProfileView.as_view(), name="profile"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path(
        "password-change/", views.PasswordChangeView.as_view(), name="password-change"
    ),
    path(
        "password-reset/",
        views.CustomResetPasswordRequestTokenView.as_view(),
        name="password-reset-request",
    ),
    path(
        "password-reset/confirm/",
        views.CustomResetPasswordConfirmView.as_view(),
        name="password-reset-confirm",
    ),
    path(
        "password-reset/validate_token/",
        views.CustomResetPasswordValidateTokenView.as_view(),
        name="password-reset-validate",
    ),
    path("files/<path:file_path>", views.S3FileView.as_view(), name="s3-file"),
]
