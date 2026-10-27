from django.core.cache import cache
from django.db.models import Avg, Count
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from users.models import User

from .models import Cart, Category, Product, Review
from .views import CATEGORY_CACHE_KEY


@receiver(post_save, sender=User)
def create_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)


@receiver(post_save, sender=Product)
def update_category_brands(sender, instance, created, **kwargs):
    if instance.category and instance.brand:
        category = instance.category
        category.brands.add(instance.brand)
        category.save()


@receiver(post_delete, sender=Product)
def delete_category_brand(sender, instance, **kwargs):
    if instance.category and instance.brand:
        category_products_with_same_brand = Product.objects.filter(
            category=instance.category, brand=instance.brand
        )
        if not category_products_with_same_brand:
            category = instance.category
            category.brands.remove(instance.brand)
            category.save()


@receiver([post_save, post_delete], sender=Category)
def invalidate_categories_cache(sender, **kwargs):
    cache.delete(CATEGORY_CACHE_KEY)


@receiver([post_save, post_delete], sender=Review)
def update_product_rating_and_count(sender, instance, **kwargs):
    product = instance.product
    stats = product.reviews.aggregate(
        avg_rating=Avg("rating"), review_count=Count("id")
    )
    updated_data = {"review_count": stats["review_count"]}

    if stats["avg_rating"] is not None:
        updated_data["rating"] = round(stats["avg_rating"], 1)
    else:
        updated_data["rating"] = None

    Product.objects.filter(id=product.id).update(**updated_data)
