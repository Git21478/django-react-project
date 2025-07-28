from . import views
from django.urls import path
from users.views import CreateUserView, PasswordChangeView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    path("user/", views.UserList.as_view(), name="user"),
    path("user/<int:pk>/", views.UserRetrieveUpdate.as_view(), name="user-update"),

    path("profile/", views.ProfileList.as_view(), name="profile"),
    path("profile/<int:pk>/", views.ProfileUpdate.as_view(), name="profile-update"),

    path("user/registration/", CreateUserView.as_view(), name="registration"),
    path("token/", TokenObtainPairView.as_view(), name="get-token"),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("password-change/", PasswordChangeView.as_view(), name="password_change"),

    path("password-reset/", PasswordResetView.as_view(), name="password_reset"),
    path("password-reset-done/", PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("password-reset-complete/", PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]