from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile
from products.models import Cart, AnonymousCart


class CustomAdminSite(AdminSite):
    site_header = "Админ панель"
    site_title = "Админ панель"
    index_title = "Магазин"

    def get_app_list(self, request):
        ordering = {
            "Товары": 1,
            "Отзывы": 2,
            "Категории": 3,
            "Бренды": 4,
            "Избранные товары": 5,
            "Избранные товары (неавторизованные пользователи)": 6,
            "Корзины": 7,
            "Корзины (неавторизованные пользователи)": 8,
            "Товары в корзине": 9,
            "Пользователи": 10,
            "Профили": 11,
        }
        app_dict = self._build_app_dict(request)
        app_list = sorted(app_dict.values(), key=lambda x: x["name"].lower())

        for app in app_list:
            app["models"].sort(key=lambda x: ordering.get(x["name"], 999))

        return app_list


class ProfileAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            None,
            {
                "fields": ["user", "avatar"],
                # "description": "<h1>Почта и аватар (description)</h1>"
            },
        ),
        ("Personal Info", {"fields": ["phone", "city"]}),
    ]
    readonly_fields = ["user", "avatar", "phone", "city"]
    list_display = ["user", "phone", "city"]
    actions = None

    # empty_value_display = ""


admin.site = CustomAdminSite(name="custom_admin")
admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
