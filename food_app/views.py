from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.core.mail import send_mail
from django.conf import settings
from decimal import Decimal
import webbrowser

from .models import FoodItem, Cart, Order


# ─────────────────────────────────────────────
#  EMAIL HELPER FUNCTIONS
# ─────────────────────────────────────────────

def send_registration_email(user):
    subject = "🍛 Welcome to FeastFlow!"
    message = f"""Hi {user.username},

Welcome to FeastFlow! 🎉

Your account has been created successfully. You can now browse our menu,
add items to your cart, and place orders anytime.

Get started: http://127.0.0.1:8000/menu/

Enjoy your meal!
— The FeastFlow Team
"""
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=True)
    except Exception:
        pass


def send_order_confirmation_email(user, order, items_summary, total, payment_method):
    payment_label = "Cash on Delivery" if payment_method == "COD" else "Online Payment"
    status_note = (
        "Your payment has been received. ✅"
        if payment_method == "ONLINE"
        else "Please keep cash ready at the time of delivery."
    )
    subject = f"🧾 FeastFlow Order Confirmed — Order #{order.id}"
    message = f"""Hi {user.username},

Your order has been placed successfully! 🎉

━━━━━━━━━━━━━━━━━━━━━━━━
  ORDER SUMMARY  (Order #{order.id})
━━━━━━━━━━━━━━━━━━━━━━━━
{items_summary}
━━━━━━━━━━━━━━━━━━━━━━━━
  Total:       ₹{total}
  Payment:     {payment_label}
  Status:      {order.status}
━━━━━━━━━━━━━━━━━━━━━━━━

{status_note}

Track your order: http://127.0.0.1:8000/orders/

— The FeastFlow Team
"""
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=True)
    except Exception:
        pass


def send_order_status_email(user, order):
    status_messages = {
        "Pending":   "Your order is pending confirmation.",
        "Paid":      "Your payment has been confirmed. ✅",
        "Preparing": "Our kitchen is now preparing your order. 🍳",
        "Delivered": "Your order has been delivered. Enjoy your meal! 🎉",
    }
    note = status_messages.get(order.status, f"Your order status is now: {order.status}")
    subject = f"📦 FeastFlow Order #{order.id} — Status Update: {order.status}"
    message = f"""Hi {user.username},

Your Order #{order.id} has been updated!

  New Status: {order.status}

{note}

View your orders: http://127.0.0.1:8000/orders/

— The FeastFlow Team
"""
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=True)
    except Exception:
        pass


# ─────────────────────────────────────────────
#  AUTHENTICATION VIEWS
# ─────────────────────────────────────────────

def register(request):
    if request.user.is_authenticated:
        return redirect('menu')

    if request.method == 'POST':
        username  = request.POST.get('username', '').strip()
        email     = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        if not username or not password1:
            messages.error(request, 'Username and password are required.')
        elif password1 != password2:
            messages.error(request, 'Passwords do not match.')
        elif len(password1) < 6:
            messages.error(request, 'Password must be at least 6 characters.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken. Choose another.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            login(request, user)
            messages.success(request, f'Welcome, {username}! Your account has been created.')
            if email:
                send_registration_email(user)
            return redirect('menu')

    return render(request, 'food_app/register.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('menu')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('menu')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'food_app/login.html')


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('login')


# ─────────────────────────────────────────────
#  MENU VIEW
# ─────────────────────────────────────────────

@login_required
def menu(request):
    food_items = FoodItem.objects.filter(is_available=True)
    categories = {}
    for item in food_items:
        cat_label = item.get_category_display()
        categories.setdefault(cat_label, []).append(item)
    return render(request, 'food_app/menu.html', {'categories': categories})


# ─────────────────────────────────────────────
#  CART VIEWS
# ─────────────────────────────────────────────

@login_required
def add_to_cart(request, food_id):
    food = get_object_or_404(FoodItem, id=food_id, is_available=True)
    cart_item, created = Cart.objects.get_or_create(
        user=request.user, food=food, defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f'"{food.name}" quantity updated in your cart.')
    else:
        messages.success(request, f'"{food.name}" added to your cart!')
    return redirect('menu')


@login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).select_related('food')
    total = sum(item.subtotal for item in cart_items)
    return render(request, 'food_app/cart.html', {'cart_items': cart_items, 'total': total})


@login_required
def update_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 1))
            if quantity < 1:
                cart_item.delete()
                messages.info(request, f'"{cart_item.food.name}" removed from cart.')
            else:
                cart_item.quantity = quantity
                cart_item.save()
                messages.success(request, 'Cart updated successfully.')
        except (ValueError, TypeError):
            messages.error(request, 'Invalid quantity entered.')
    return redirect('cart')


@login_required
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    food_name = cart_item.food.name
    cart_item.delete()
    messages.info(request, f'"{food_name}" has been removed from your cart.')
    return redirect('cart')


# ─────────────────────────────────────────────
#  ORDER VIEWS
# ─────────────────────────────────────────────

@login_required
def place_order(request):
    cart_items = Cart.objects.filter(user=request.user).select_related('food')

    if not cart_items.exists():
        messages.warning(request, 'Your cart is empty. Add items before placing an order.')
        return redirect('cart')

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method', 'COD')
        if payment_method not in ['COD', 'ONLINE']:
            payment_method = 'COD'

        total = sum(item.subtotal for item in cart_items)
        summary_lines = [
            f"{item.food.name} × {item.quantity} = ₹{item.subtotal}"
            for item in cart_items
        ]
        items_summary = '\n'.join(summary_lines)
        status = 'Paid' if payment_method == 'ONLINE' else 'Pending'

        order = Order.objects.create(
            user=request.user,
            total_amount=total,
            payment_method=payment_method,
            status=status,
            items_summary=items_summary,
        )

        cart_items.delete()

        if payment_method == 'ONLINE':
            messages.success(request, '🎉 Payment successful! Your order has been placed.')
        else:
            messages.success(request, '✅ Order placed! Pay cash upon delivery.')

        if request.user.email:
            send_order_confirmation_email(request.user, order, items_summary, total, payment_method)

        return redirect('order_list')

    return redirect('cart')


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    delivered_count = orders.filter(status='Delivered').count()
    return render(request, 'food_app/orders.html', {'orders': orders, 'delivered_count': delivered_count})