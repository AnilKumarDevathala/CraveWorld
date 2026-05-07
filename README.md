# 🍛 FeastFlow — Food Ordering Web Application
### Django + MySQL | Full-Stack Mini Project

---

## 📋 Project Structure

```
food_ordering/
├── manage.py
├── requirements.txt
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
        ├── base.html         ← Shared layout + navbar
        ├── login.html
        ├── register.html
        ├── menu.html
        ├── cart.html
        └── orders.html
```

---

## ⚙️ Setup Instructions

### Step 1 — Install Python & Django
```bash
pip install django mysqlclient
# OR
pip install -r requirements.txt
```

### Step 2 — Create MySQL Database
Open MySQL Workbench or terminal and run:
```sql
CREATE DATABASE food_ordering_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Step 3 — Configure Database
Edit `food_ordering/settings.py` and update:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'food_ordering_db',   # your DB name
        'USER': 'root',               # your MySQL user
        'PASSWORD': 'yourpassword',   # your MySQL password
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### Step 4 — Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5 — Create Admin User
```bash
python manage.py createsuperuser
```

### Step 6 — Populate Sample Food Items
```bash
python manage.py shell < populate_data.py
```

### Step 7 — Run the Server
```bash
python manage.py runserver
```

Visit → **http://127.0.0.1:8000**

---

## 🌐 URL Map

| URL                | View           | Description              |
|--------------------|----------------|--------------------------|
| `/`                | login_view     | Login page               |
| `/register/`       | register       | Create account           |
| `/logout/`         | logout_view    | Sign out                 |
| `/menu/`           | menu           | Browse food items        |
| `/cart/`           | cart           | View cart                |
| `/add/<id>/`       | add_to_cart    | Add item to cart         |
| `/update/<id>/`    | update_cart    | Update quantity          |
| `/remove/<id>/`    | remove_from_cart | Remove item from cart  |
| `/place-order/`    | place_order    | Checkout & place order   |
| `/orders/`         | order_list     | View order history       |
| `/admin/`          | Django Admin   | Admin panel              |

---

## 🗄️ Database Models

### FoodItem
| Field        | Type         | Notes                    |
|--------------|--------------|--------------------------|
| name         | CharField    | Food name                |
| description  | TextField    | Description              |
| price        | DecimalField | In ₹                     |
| category     | CharField    | starters/mains/desserts/drinks |
| is_available | BooleanField | Show/hide on menu        |

### Cart
| Field     | Type          | Notes                          |
|-----------|---------------|--------------------------------|
| user      | ForeignKey    | Links to Django User           |
| food      | ForeignKey    | Links to FoodItem              |
| quantity  | PositiveIntegerField | Quantity ordered        |
| added_at  | DateTimeField | Auto-set on creation           |

### Order
| Field          | Type         | Notes                        |
|----------------|--------------|------------------------------|
| user           | ForeignKey   | Who placed the order         |
| total_amount   | DecimalField | Total in ₹                   |
| payment_method | CharField    | COD or ONLINE                |
| status         | CharField    | Pending/Paid/Preparing/Delivered |
| items_summary  | TextField    | Snapshot of items ordered    |
| created_at     | DateTimeField| Auto-set on creation         |

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

---

## 🎨 UI Design

- **Theme**: Dark mode with amber/orange accent
- **Fonts**: Playfair Display (headings) + DM Sans (body)
- **Responsive**: Works on mobile and desktop
- **Animations**: Smooth card entrances and transitions

---

## 👨‍💻 Admin Panel Tips

1. Go to `http://127.0.0.1:8000/admin/`
2. Log in with your superuser credentials
3. Under **Food App**:
   - Add/edit food items
   - Monitor cart items
   - Update order statuses

---

*Built with Django 4.x + MySQL | Mini Project Assignment*
