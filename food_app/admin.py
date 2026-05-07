from django.contrib import admin
from .models import FoodItem, Cart, Order


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_available')
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'description')
    list_editable = ('price', 'is_available')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'food', 'quantity', 'added_at')
    list_filter = ('user',)
    search_fields = ('user__username', 'food__name')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_amount', 'payment_method', 'status', 'created_at')
    list_filter = ('status', 'payment_method')
    search_fields = ('user__username',)
    list_editable = ('status',)
