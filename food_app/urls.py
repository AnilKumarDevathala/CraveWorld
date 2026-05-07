from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Menu
    path('menu/', views.menu, name='menu'),

    # Cart
    path('cart/', views.cart, name='cart'),
    path('add/<int:food_id>/', views.add_to_cart, name='add_to_cart'),
    path('update/<int:cart_id>/', views.update_cart, name='update_cart'),
    path('remove/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),

    # Orders
    path('place-order/', views.place_order, name='place_order'),
    path('orders/', views.order_list, name='order_list'),
]
