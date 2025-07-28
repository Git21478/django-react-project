from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from .custom_classes import AbstractUser

class User(AbstractUser):
    email = models.EmailField(max_length=100, unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="profile", verbose_name="Пользователь")
    avatar = models.ImageField(default="profile_avatars/default_avatar.png", upload_to="profile_avatars/uploaded")
    phone = models.CharField(verbose_name="Номер телефона", unique=True, blank=True, null=True, validators=[
        MinLengthValidator(1),
        MaxLengthValidator(12)
    ])
    city = models.CharField(max_length=100, blank=True, default="", verbose_name="Город")

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

        constraints = [
            models.CheckConstraint(
                condition=models.Q(phone__lte=12),
                name="phone_lte_12"
            )
        ]

    def __str__(self):
        return self.user.username