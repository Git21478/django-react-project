from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from .models import Brand, Category, Product, Review, FavoriteProduct, CartProduct
from users.admin import CustomAdminSite

class BrandAdmin(admin.ModelAdmin):
    pass

class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    filter_horizontal = ["brands"] # filter_vertical

class ProductAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Фото", {
            "fields": ["image"],
        }),
        ("Информация о товаре", {
            "fields": ["name", "description", "price", ("category", "brand"), "slug"],
        }),
    ]
    list_display = ["name", "price", "category", "brand", "slug"]
    list_filter = ["price", "category", "brand"]
    list_editable = ["price"]
    search_fields = ["name", "price", "category__name", "brand__name"]
    # search_help_text = "hahaha"
    show_full_result_count = False
    show_facets = admin.ShowFacets.ALWAYS # Always / Allow (default) / Never
    radio_fields = {"category": admin.VERTICAL, "brand": admin.VERTICAL}
    save_as = True
    # save_as_continue = False
    # save_on_top = True

class ReviewAdmin(admin.ModelAdmin):
    readonly_fields = ["title", "content", "rating", "product", "author", "created_at"]
    list_display = ["title", "rating", "product", "author", "created_at"]
    list_filter = ["rating", "product", "author", "created_at"]
    search_fields = ["title", "rating", "product__name", "author__email"]
    date_hierarchy = "created_at"
    # exclude = ["author", "product"]

class FavoriteProductAdmin(admin.ModelAdmin):
    list_display = ["product", "user"]

class CartProductAdmin(admin.ModelAdmin):
    list_display = ["product", "quantity", "get_product_price", "user"]

admin.site.register(Brand, BrandAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(FavoriteProduct, FavoriteProductAdmin)
admin.site.register(CartProduct, CartProductAdmin)