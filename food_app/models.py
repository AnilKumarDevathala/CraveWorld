from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail


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


@receiver(post_save, sender=Order)
def notify_admin(sender, instance, created, **kwargs):
    if created:
        subject = f"🆕 New Order #{instance.id} by {instance.user.username}"
        message = f"New order placed!\n\nOrder ID: #{instance.id}\nUser: {instance.user.username}\nTotal: ₹{instance.total_amount}\nPayment: {instance.get_payment_method_display()}\nItems: {instance.items_summary}"
    else:
        subject = f"🔄 Order #{instance.id} changed to {instance.status}"
        message = f"Order updated!\n\nOrder ID: #{instance.id}\nUser: {instance.user.username}\nTotal: ₹{instance.total_amount}\nNew Status: {instance.status}\nItems: {instance.items_summary}"

    send_mail(subject, message, settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], fail_silently=True)