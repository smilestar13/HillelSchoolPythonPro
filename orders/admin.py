from django.contrib import admin
from django.contrib.admin import TabularInline

from orders.models import Order, OrderItem, Discount


class OrderItemInline(TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('total_amount', 'user', 'discount', 'is_active')
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'price', 'quantity')


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('amount', 'code', 'is_active')
