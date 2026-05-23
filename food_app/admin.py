from django.contrib import admin
from .models import FoodItem, Cart, Order
from food_app.views import send_order_status_email

@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_available']
    list_filter = ['category', 'is_available']
    search_fields = ['name']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'food', 'quantity', 'added_at']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_amount', 'payment_method', 'status', 'created_at']
    list_filter = ['status', 'payment_method']

    def save_model(self, request, obj, form, change):
        if change and 'status' in form.changed_data:
            super().save_model(request, obj, form, change)
            if obj.user.email:
                send_order_status_email(obj.user, obj)
        else:
            super().save_model(request, obj, form, change)