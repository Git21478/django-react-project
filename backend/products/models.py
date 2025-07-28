from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator
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
        if self.price < 0:
            raise ValidationError("Price can't be negative")
    
    def get_rating(self):
        reviews = Review.objects.filter(product=self)
        review_amount = len(reviews)
        if review_amount != 0:
            rating = sum([review.rating for review in reviews]) / review_amount
            rating = round(rating, 2)
            return rating
        return None
    
    def get_review_amount(self):
        review_amount = len(Review.objects.filter(product=self.id))
        return review_amount
    
    def get_favorite_product_id(self, current_user):
        favorite_product = FavoriteProduct.objects.filter(user=current_user.id, product=self.id).first()
        if favorite_product:
            return favorite_product.id
        else:
            return None

    def get_cart_product_id(self, current_user):
        cart_product = CartProduct.objects.filter(user=current_user.id, product=self.id).first()
        if cart_product:
            return cart_product.id
        else:
            return None
    
    def get_is_favorite_product(self, current_user):
        is_favorite_product = False
        favorite_product_objects = FavoriteProduct.objects.filter(user=current_user.id)
        favorite_products = [favorite_product_object.product for favorite_product_object in favorite_product_objects]
        if self in favorite_products:
            is_favorite_product = True
        return is_favorite_product
    
    def get_is_cart_product(self, current_user):
        is_cart_product = False
        cart_product_objects = CartProduct.objects.filter(user=current_user.id)
        cart_products = [cart_product_object.product for cart_product_object in cart_product_objects]
        if self in cart_products:
            is_cart_product = True
        return is_cart_product

class Review(models.Model):
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    content = models.TextField(max_length=1000)
    rating = models.PositiveSmallIntegerField(verbose_name="Оценка", validators=[
        MinValueValidator(limit_value=1),
        MaxValueValidator(limit_value=5),
    ])
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews", verbose_name="Автор отзыва")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews", verbose_name="Отзыв к товару")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return self.title

#Favorites
class FavoriteProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="favorite_products", verbose_name="Пользователь")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="favorite_products", verbose_name="Товар")

    class Meta:
        verbose_name = "Избранный товар"
        verbose_name_plural = "Избранные товары"
    
    def __str__(self):
        return Product.objects.get(id=self.product.id).name

#Cart
class CartProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="cart_products", verbose_name="Пользователь")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_products", verbose_name="Товар")
    quantity = models.PositiveSmallIntegerField(verbose_name="Количество товара", default=1)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        verbose_name = "Товар в корзине"
        verbose_name_plural = "Товары в корзине"
    
    def __str__(self):
        return Product.objects.get(id=self.product.id).name
    
    def get_product_price(self):
        return Product.objects.get(id=self.product.id).price

    get_product_price.short_description = "Цена"

    def get_total_quantity(self, current_user):
        current_user_cart_products = CartProduct.objects.filter(user=current_user.id)
        total_quantity = 0
        for cart_product in current_user_cart_products:
            total_quantity += cart_product.quantity
        return total_quantity

    def get_total_price(self, current_user):
        current_user_cart_products = CartProduct.objects.filter(user=current_user.id)
        total_price = 0
        for cart_product in current_user_cart_products:
            total_price += cart_product.product.price * cart_product.quantity
        return total_price