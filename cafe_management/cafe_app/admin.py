# cafe_app/admin.py

from django.contrib import admin
from .models import MenuItem, Order, OrderItem, Bill

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'stock', 'available')
    list_filter = ('category', 'available')
    search_fields = ('name',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'payment_method', 'total_price')
    list_filter = ('payment_method',)
    search_fields = ('customer_name',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'menu_item', 'quantity')
    list_filter = ('menu_item',)
    search_fields = ('order__customer_name', 'menu_item__name')

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'total_amount', 'payment_method', 'generated_at')
    list_filter = ('payment_method',)
    search_fields = ('order__customer_name',)
