from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from decimal import Decimal

from .models import FoodItem, Cart, Order


# ─────────────────────────────────────────────
#  AUTHENTICATION VIEWS
# ─────────────────────────────────────────────

def register(request):
    """Create a new user account."""
    if request.user.is_authenticated:
        return redirect('menu')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
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
            return redirect('menu')

    return render(request, 'food_app/register.html')


def login_view(request):
    """Log in an existing user."""
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
    """Log out the current user."""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('login')


# ─────────────────────────────────────────────
#  MENU VIEW
# ─────────────────────────────────────────────

@login_required
def menu(request):
    """Display all available food items grouped by category."""
    food_items = FoodItem.objects.filter(is_available=True)
    cart_count = Cart.objects.filter(user=request.user).count()

    # Group by category for template
    categories = {}
    for item in food_items:
        cat_label = item.get_category_display()
        categories.setdefault(cat_label, []).append(item)

    context = {
        'categories': categories,
        'cart_count': cart_count,
    }
    return render(request, 'food_app/menu.html', context)


# ─────────────────────────────────────────────
#  CART VIEWS
# ─────────────────────────────────────────────

@login_required
def add_to_cart(request, food_id):
    """Add a food item to the cart or increment quantity."""
    food = get_object_or_404(FoodItem, id=food_id, is_available=True)
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        food=food,
        defaults={'quantity': 1}
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
    """Show all items in the user's cart with total price."""
    cart_items = Cart.objects.filter(user=request.user).select_related('food')
    total = sum(item.subtotal for item in cart_items)
    cart_count = cart_items.count()

    context = {
        'cart_items': cart_items,
        'total': total,
        'cart_count': cart_count,
    }
    return render(request, 'food_app/cart.html', context)


@login_required
def update_cart(request, cart_id):
    """Update the quantity of a cart item."""
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
    """Remove an item from the cart."""
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
    """Convert all cart items into a placed order."""
    cart_items = Cart.objects.filter(user=request.user).select_related('food')

    if not cart_items.exists():
        messages.warning(request, 'Your cart is empty. Add items before placing an order.')
        return redirect('cart')

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method', 'COD')
        if payment_method not in ['COD', 'ONLINE']:
            payment_method = 'COD'

        # Calculate total
        total = sum(item.subtotal for item in cart_items)

        # Build summary snapshot
        summary_lines = [
            f"{item.food.name} × {item.quantity} = ₹{item.subtotal}"
            for item in cart_items
        ]
        items_summary = '\n'.join(summary_lines)

        # Determine status
        status = 'Paid' if payment_method == 'ONLINE' else 'Pending'

        # Create order
        Order.objects.create(
            user=request.user,
            total_amount=total,
            payment_method=payment_method,
            status=status,
            items_summary=items_summary,
        )

        # Clear cart
        cart_items.delete()

        if payment_method == 'ONLINE':
            messages.success(request, '🎉 Payment successful! Your order has been placed.')
        else:
            messages.success(request, '✅ Order placed! Pay cash upon delivery.')

        return redirect('order_list')

    # GET: show confirmation page (rendered inside cart.html with modal)
    return redirect('cart')


@login_required
def order_list(request):
    """Show all past orders for the logged-in user."""
    orders = Order.objects.filter(user=request.user)
    cart_count = Cart.objects.filter(user=request.user).count()

    context = {
        'orders': orders,
        'cart_count': cart_count,
    }
    return render(request, 'food_app/orders.html', context)
