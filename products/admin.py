from django.contrib import admin

from products.models import Product, Category
from project.mixins.admins import ImageSnapshotAdminMixin


@admin.register(Product)
class ProductAdmin(ImageSnapshotAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'price', 'is_active')
    filter_horizontal = ('categories', 'products')
    readonly_fields = ('image_tag', )


@admin.register(Category)
class CategoryAdmin(ImageSnapshotAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'description')
    readonly_fields = ('image_tag', )
