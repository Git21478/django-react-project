from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


class Brand(models.Model):
    name = models.CharField(max_length=100, verbose_name="Бренд")

    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Категория")
    slug = models.SlugField(max_length=100, unique=True)
    brands = models.ManyToManyField(Brand, blank=True, related_name="categories")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Product(models.Model):
    image = models.ImageField(upload_to="product_images/")
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="products",
        verbose_name="Категория",
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="products",
        verbose_name="Производитель",
    )
    slug = models.SlugField(max_length=100, unique=True)
    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        null=True,
        blank=True,
        default=None,
        verbose_name="Рейтинг",
    )
    review_count = models.IntegerField(default=0, verbose_name="Количество отзывов")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        constraints = [
            models.CheckConstraint(condition=models.Q(price__gt=0), name="price_gt_0")
        ]

    def __str__(self):
        return self.name

    def clean(self):
        if self.price <= 0:
            raise ValidationError("Price should be a positive number")

    def _get_session_key(self, request):
        if request and request.session:
            return request.session.session_key
        return None

    def get_favorite_id(self, request):
        if not request:
            return None
        
        if request.user.is_authenticated:
            favorite = Favorite.objects.filter(user=request.user, product=self).first()
            return favorite.id if favorite else None

        session_key = self._get_session_key(request)
        if session_key:
            favorite = Favorite.objects.filter(
                session_key=session_key, user__isnull=True, product=self
            ).first()
            return favorite.id if favorite else None
        return None

    def get_cart_product_id(self, request):
        if not request:
            return None
        
        if request.user.is_authenticated:
            cart_product = CartProduct.objects.filter(
                cart__user=request.user, product=self
            ).first()
            return cart_product.id if cart_product else None

        session_key = self._get_session_key(request)
        if session_key:
            cart_product = CartProduct.objects.filter(
                cart__session_key=session_key, cart__user__isnull=True, product=self
            ).first()
            return cart_product.id if cart_product else None
        return None

    def get_is_favorite(self, request):
        return self.get_favorite_id(request) is not None

    def get_is_cart_product(self, request):
        return self.get_cart_product_id(request) is not None


class Review(models.Model):
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    content = models.TextField(max_length=1000)
    rating = models.PositiveSmallIntegerField(
        verbose_name="Оценка",
        validators=[
            MinValueValidator(limit_value=1),
            MaxValueValidator(limit_value=5),
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время")
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Отзыв к товару",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Автор отзыва",
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        constraints = [
            models.UniqueConstraint(
                fields=["product", "author"],
                name="unique_product_author_review",
            )
        ]

    def __str__(self):
        return self.title


# Favorites
class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name="Пользователь",
        null=True,
        blank=True,
    )
    session_key = models.CharField(
        max_length=40, db_index=True, null=True, blank=True, verbose_name="Сессия"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name="Товар",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Избранный товар"
        verbose_name_plural = "Избранные товары"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "product"],
                name="unique_user_product",
                condition=models.Q(user__isnull=False),
            ),
            models.UniqueConstraint(
                fields=["session_key", "product"],
                name="unique_session_product",
                condition=models.Q(user__isnull=True),
            ),
        ]

    def __str__(self):
        return self.product.name


# Cart
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name="cart")
    session_key = models.CharField(
        max_length=40, db_index=True, null=True, blank=True, verbose_name="Сессия"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"
        constraints = [
            models.UniqueConstraint(
                fields=["session_key"],
                name="unique_session_cart",
                condition=models.Q(user__isnull=True),
            ),
            models.CheckConstraint(
                condition=models.Q(user__isnull=False)
                | models.Q(session_key__isnull=False),
                name="cart_has_user_or_session",
            ),
        ]

    @property
    def total_price(self):
        return sum(product.total_price for product in self.products.all())

    @property
    def total_quantity(self):
        return sum(product.quantity for product in self.products.all())

    def __str__(self):
        if self.user:
            return f"Корзина пользователя {self.user.username}"
        return f"Корзина анонимного пользователя {self.session_key[:8]}..."


class CartProduct(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="products",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="cart_products",
        verbose_name="Товар",
    )
    quantity = models.PositiveSmallIntegerField(
        verbose_name="Количество товара", default=1
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        verbose_name = "Товар в корзине"
        verbose_name_plural = "Товары в корзине"
        unique_together = ["cart", "product"]
        ordering = ["-created_at"]

    def __str__(self):
        return self.product.name

    @property
    def total_price(self):
        return self.product.price * self.quantity
