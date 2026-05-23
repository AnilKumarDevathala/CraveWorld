# 🍛 CraveWorld — Food Ordering Web Application
### Django + MySQL | Full-Stack Mini Project

---

## 📋 Project Structure

food_ordering/
├── manage.py
├── requirements.txt
├── .env.example              ← Copy this to .env and fill your details
├── populate_data.py          ← Run this to add sample menu items
├── food_ordering/            ← Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── food_app/                 ← Main application
    ├── models.py             ← FoodItem, Cart, Order
    ├── views.py              ← All backend logic
    ├── urls.py               ← URL routing
    ├── admin.py              ← Admin panel config
    └── templates/food_app/
        ├── base.html
        ├── login.html
        ├── register.html
        ├── menu.html
        ├── cart.html
        └── orders.html

---

## ⚙️ Setup Instructions

### Step 1 — Install dependencies
pip install django mysqlclient python-decouple
# OR
pip install -r requirements.txt

### Step 2 — Create MySQL Database
CREATE DATABASE food_ordering_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

### Step 3 — Setup Environment Variables
Copy .env.example to .env and fill your details:
cp .env.example .env

Edit .env:
EMAIL_HOST_USER=your-gmail@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
DB_USER=root
DB_PASSWORD=your-mysql-password
DJANGO_SECRET_KEY=your-secret-key

### Step 4 — Run Migrations
python manage.py makemigrations
python manage.py migrate

### Step 5 — Create Admin User
python manage.py createsuperuser

### Step 6 — Populate Sample Food Items
python manage.py shell < populate_data.py

### Step 7 — Run the Server
python manage.py runserver

Visit → http://127.0.0.1:8000

---

## ✅ Features Implemented

- [x] User Registration & Login (Django auth)
- [x] Logout
- [x] Menu page grouped by category
- [x] Add to Cart (increments quantity if already in cart)
- [x] Cart page with quantity controls
- [x] Update cart item quantity (CRUD)
- [x] Remove item from cart (CRUD)
- [x] Place order with payment method (COD / Online simulation)
- [x] Order history page
- [x] Admin panel for managing all data
- [x] Flash messages for all actions
- [x] Responsive dark-themed UI
- [x] Email notifications (order confirmation + status updates)

---

## 📧 Email Setup (Gmail)

1. Enable 2-Step Verification on your Google account
2. Go to myaccount.google.com/apppasswords
3. Generate an App Password
4. Paste it in your .env file as EMAIL_HOST_PASSWORD

---

## 🌐 URL Map

| URL                | View             | Description            |
|--------------------|------------------|------------------------|
| /                  | login_view       | Login page             |
| /register/         | register         | Create account         |
| /logout/           | logout_view      | Sign out               |
| /menu/             | menu             | Browse food items      |
| /cart/             | cart             | View cart              |
| /add/<id>/         | add_to_cart      | Add item to cart       |
| /update/<id>/      | update_cart      | Update quantity        |
| /remove/<id>/      | remove_from_cart | Remove item from cart  |
| /place-order/      | place_order      | Checkout & place order |
| /orders/           | order_list       | View order history     |
| /admin/            | Django Admin     | Admin panel            |

---

*Built with Django 6.x + MySQL | Mini Project Assignment*