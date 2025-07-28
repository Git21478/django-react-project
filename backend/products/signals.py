from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from .models import Product, Category

@receiver(post_save, sender=Product)
def update_category_brands(sender, instance, created, **kwargs):
    if created and instance.category and instance.brand:
        category = instance.category
        category.brands.add(instance.brand)
        category.save()

# @receiver(post_delete, sender=Product)
# def delete_category_brand(sender, instance, **kwargs):
#     if instance.category and instance.brand:
#         category = instance.category
#         current_category_products = Product.objects.filter(category=category)
#         print(current_category_products)
#         print(current_category_products)
#         print(current_category_products)
#         if not current_category_products:
#             category.brands.remove(instance.brand)
#             category.save()