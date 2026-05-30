from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
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
    image = models.ImageField(default="product_images/product_image.jpg", upload_to="product_images/uploaded")
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name="products", verbose_name="Категория")
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, blank=True, null=True, related_name="products", verbose_name="Производитель")
    slug = models.SlugField(max_length=100, unique=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True, default=None, verbose_name="Рейтинг")
    review_count = models.IntegerField(default=0, verbose_name="Количество отзывов")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

        constraints = [
            models.CheckConstraint(
                condition=models.Q(price__gt=0),
                name="price_gt_0"
            )
        ]

    def __str__(self):
        return self.name

    def clean(self):
        if self.price <= 0:
            raise ValidationError("Price should be a positive number")
    
    def get_favorite_id(self, current_user):
        if current_user.is_authenticated:
            favorite = Favorite.objects.filter(user=current_user.id, product=self.id).first()
            return favorite.id if favorite else None
        else:
            session_key = self.request.session.session_key
            if session_key:
                favorite = AnonymousFavorite.objects.filter(session_key=session_key, product=self.id).first()
                return favorite.id if favorite else None
            else:
                return None

    def get_cart_product_id(self, current_user):
        if current_user.is_authenticated:
            cart_product = CartProduct.objects.filter(cart__user=current_user.id, product=self.id).first()
            return cart_product.id if cart_product else None
        else:
            session_key = self.request.session.session_key
            if session_key:
                cart_product = CartProduct.objects.filter(anonymous_cart__session_key=session_key, product=self.id).first()
                return cart_product.id if cart_product else None
            else:
                return None
    
    def get_is_favorite(self, current_user):
        if current_user.is_authenticated:
            return Favorite.objects.filter(user=current_user.id, product=self.id).exists()
        else:
            session_key = self.request.session.session_key
            if session_key:
                return AnonymousFavorite.objects.filter(session_key=session_key, product=self.id).exists()
    
    def get_is_cart_product(self, current_user):
        if current_user.is_authenticated:
            return CartProduct.objects.filter(cart__user=current_user.id, product=self.id).exists()
        else:
            session_key = self.request.session.session_key
            if session_key:
                return CartProduct.objects.filter(anonymous_cart__session_key=session_key, product=self.id).exists()
            
        return CartProduct.objects.filter(user=current_user.id, product=self.id).exists()

class Review(models.Model):
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    content = models.TextField(max_length=1000)
    rating = models.PositiveSmallIntegerField(verbose_name="Оценка", validators=[
        MinValueValidator(limit_value=1),
        MaxValueValidator(limit_value=5),
    ])
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews", verbose_name="Отзыв к товару")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews", verbose_name="Автор отзыва")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        unique_together = ["product", "author"]

    def __str__(self):
        return self.title

#Favorites
class BaseFavorite(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        verbose_name = "Избранный товар"
        verbose_name_plural = "Избранные товары"
    
    def __str__(self):
        return self.product.name    

class Favorite(BaseFavorite):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites", verbose_name="Пользователь")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="favorites", verbose_name="Товар")

    class Meta:
        verbose_name = "Избранный товар"
        verbose_name_plural = "Избранные товары"
        unique_together = ["user", "product"]
    
class AnonymousFavorite(BaseFavorite):
    session_key = models.CharField(max_length=40, db_index=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="anonymous_favorites", verbose_name="Товар")

    class Meta:
        verbose_name = "Избранный товар (неавторизованные пользователи)"
        verbose_name_plural = "Избранные товары (неавторизованные пользователи)"
        unique_together = ["session_key", "product"]

#Cart
class BaseCart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:  
        abstract = True

    @property
    def total_price(self):
        return sum(product.total_price for product in self.products.all())
    
    @property
    def total_quantity(self):
        return sum(product.quantity for product in self.products.all())
    
class Cart(BaseCart):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

class AnonymousCart(BaseCart):
    session_key = models.CharField(max_length=40, unique=True, db_index=True)

    class Meta:
        verbose_name = "Корзина (неавторизованный пользователь)"
        verbose_name_plural = "Корзины (неавторизованные пользователи)"
        

class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True, related_name="products")
    anonymous_cart = models.ForeignKey(AnonymousCart, on_delete=models.CASCADE, null=True, blank=True, related_name="products")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_products", verbose_name="Товар")
    quantity = models.PositiveSmallIntegerField(verbose_name="Количество товара", default=1)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        verbose_name = "Товар в корзине"
        verbose_name_plural = "Товары в корзине"
        unique_together = [["cart", "product"], ["anonymous_cart", "product"]]
        ordering = ["-created_at"]
    
    def __str__(self):
        return Product.objects.get(id=self.product.id).name

    @property
    def total_price(self):
        return self.product.price * self.quantity