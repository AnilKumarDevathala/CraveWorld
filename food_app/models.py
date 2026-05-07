from django.db import models
from django.contrib.auth.models import User


class FoodItem(models.Model):
    """Represents a food item available on the menu."""
    CATEGORY_CHOICES = [
        ('starters', 'Starters'),
        ('mains', 'Main Course'),
        ('desserts', 'Desserts'),
        ('drinks', 'Drinks'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='mains')
    image_url = models.URLField(blank=True, null=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} (₹{self.price})"

    class Meta:
        ordering = ['category', 'name']


class Cart(models.Model):
    """Stores food items a user has added before placing an order."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    food = models.ForeignKey(FoodItem, on_delete=models.CASCADE, related_name='cart_entries')
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} → {self.food.name} × {self.quantity}"

    @property
    def subtotal(self):
        return self.food.price * self.quantity

    class Meta:
        unique_together = ('user', 'food')
        ordering = ['-added_at']


class Order(models.Model):
    """Represents a placed order after checkout."""
    PAYMENT_CHOICES = [
        ('COD', 'Cash on Delivery'),
        ('ONLINE', 'Online Payment'),
    ]
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Preparing', 'Preparing'),
        ('Delivered', 'Delivered'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='COD')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    # Store snapshot of ordered items as text summary
    items_summary = models.TextField(blank=True, default='')

    def __str__(self):
        return f"Order #{self.id} by {self.user.username} — ₹{self.total_amount}"

    class Meta:
        ordering = ['-created_at']
