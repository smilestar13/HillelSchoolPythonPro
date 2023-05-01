from django.contrib import admin
from django.contrib.admin import TabularInline

from wishes.models import WishList, WishListItem


class WishListItemInline(TabularInline):
    model = WishListItem
    extra = 1


@admin.register(WishList)
class WishesAdmin(admin.ModelAdmin):
    list_display = ('total_amount', 'user', 'discount', 'is_active')
    inlines = [WishListItemInline]


@admin.register(WishListItem)
class WishesItemAdmin(admin.ModelAdmin):
    list_display = ('wish_list', 'product', 'price', 'quantity')
