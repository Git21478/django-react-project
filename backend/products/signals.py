from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from .models import Product, Cart, AnonymousCart
from users.models import User
from django.contrib.sessions.models import Session

@receiver(post_save, sender=User)
def create_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)

@receiver(post_save, sender=Session)
def create_anonymous_cart(sender, instance, created, **kwargs):
    if created:
        AnonymousCart.objects.get_or_create(session_key=instance.session_key)

@receiver(post_save, sender=Product)
def update_category_brands(sender, instance, created, **kwargs):
    if instance.category and instance.brand:
        category = instance.category
        category.brands.add(instance.brand)
        category.save()

@receiver(post_delete, sender=Product)
def delete_category_brand(sender, instance, **kwargs):
    if instance.category and instance.brand:
        category_products_with_same_brand = Product.objects.filter(category=instance.category, brand=instance.brand)
        if not category_products_with_same_brand:
            category = instance.category
            category.brands.remove(instance.brand)
            category.save()