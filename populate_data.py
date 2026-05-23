"""
Run this script to populate the database with sample food items.

Usage:
    python manage.py shell < populate_data.py
    OR
    python manage.py runscript populate_data  (with django-extensions)

Or just copy-paste into the Django shell:
    python manage.py shell
"""

import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_ordering.settings')
django.setup()

from food_app.models import FoodItem

# Clear existing items (optional)
# FoodItem.objects.all().delete()

sample_items = [
    # Starters
    {'name': 'Paneer Tikka',        'category': 'starters', 'price': 220, 'description': 'Succulent cottage cheese cubes marinated in spiced yogurt and grilled in a tandoor until perfectly charred.', 'image_url': 'https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8?w=400&q=80'},
    {'name': 'Veg Spring Rolls',    'category': 'starters', 'price': 150, 'description': 'Crispy golden rolls stuffed with stir-fried vegetables, ginger, and soy sauce.', 'image_url': 'https://images.unsplash.com/photo-1607330289024-1535c6b4e1c1?w=400&q=80'},
    {'name': 'Chicken Lollipop',    'category': 'starters', 'price': 280, 'description': 'Indo-Chinese classic — chicken wings shaped like lollipops, deep-fried and tossed in chilli sauce.', 'image_url': 'https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?w=400&q=80'},
    {'name': 'Hara Bhara Kabab',    'category': 'starters', 'price': 180, 'description': 'Soft, flavourful patties made with spinach, green peas, and paneer, shallow-fried to perfection.', 'image_url': 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=400&q=80'},

    # Main Course
    {'name': 'Butter Chicken',      'category': 'mains', 'price': 320, 'description': 'Tender chicken in a velvety tomato-butter gravy with aromatic spices. Pairs beautifully with naan.', 'image_url': 'https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?w=400&q=80'},
    {'name': 'Dal Makhani',         'category': 'mains', 'price': 240, 'description': 'Slow-cooked black lentils simmered overnight with butter and cream — a North Indian staple.', 'image_url': 'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=400&q=80'},
    {'name': 'Palak Paneer',        'category': 'mains', 'price': 260, 'description': 'Fresh cottage cheese cubes in a vibrant spinach gravy spiced with cumin and garam masala.', 'image_url': 'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=400&q=80'},
    {'name': 'Chicken Biryani',     'category': 'mains', 'price': 350, 'description': 'Fragrant basmati rice layered with marinated chicken, caramelised onions, and saffron.', 'image_url': 'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=400&q=80'},
    {'name': 'Veg Fried Rice',      'category': 'mains', 'price': 190, 'description': 'Wok-tossed rice with fresh vegetables, egg, and house soy sauce blend.', 'image_url': 'https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=400&q=80'},
    {'name': 'Mutton Rogan Josh',   'category': 'mains', 'price': 420, 'description': 'A Kashmiri signature — tender mutton slow-cooked in a rich sauce of whole spices and Kashmiri chillies.', 'image_url': 'https://images.unsplash.com/photo-1545247181-516773cae754?w=400&q=80'},
    {'name': 'Masala Dosa',         'category': 'mains', 'price': 160, 'description': 'Crispy rice crepe stuffed with spiced mashed potatoes, served with sambar and chutneys.', 'image_url': 'https://images.unsplash.com/photo-1630383249896-424e482df921?w=400&q=80'},

    # Desserts
    {'name': 'Gulab Jamun',         'category': 'desserts', 'price': 90, 'description': 'Soft milk-solid dumplings soaked in rose-cardamom sugar syrup. Best served warm.', 'image_url': 'https://images.unsplash.com/photo-1666365350010-05bcb1ffa313?w=400&q=80'},
    {'name': 'Chocolate Lava Cake', 'category': 'desserts', 'price': 180, 'description': 'Warm chocolate cake with a gooey molten centre, served with a scoop of vanilla ice cream.', 'image_url': 'https://images.unsplash.com/photo-1606313564200-e75d5e30476c?w=400&q=80'},
    {'name': 'Mango Kulfi',         'category': 'desserts', 'price': 110, 'description': 'Traditional Indian ice cream made with condensed milk, flavoured with fresh Alphonso mango.', 'image_url': 'https://images.unsplash.com/photo-1615832494873-b0c52d519696?w=400&q=80'},
    {'name': 'Rasgulla',            'category': 'desserts', 'price': 80, 'description': 'Light, spongy cottage cheese balls simmered in a fragrant sugar syrup.', 'image_url': 'https://images.unsplash.com/photo-1674479862960-b4180bcc2dce?w=400&q=80'},

    # Drinks
    {'name': 'Mango Lassi',         'category': 'drinks', 'price': 100, 'description': 'Thick, creamy blend of fresh mango pulp, yogurt, and a hint of cardamom.', 'image_url': 'https://images.unsplash.com/photo-1527661591475-527312dd65f5?w=400&q=80'},
    {'name': 'Masala Chai',         'category': 'drinks', 'price': 60,  'description': 'Classic Indian spiced tea brewed with ginger, cardamom, cinnamon, and milk.', 'image_url': 'https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=400&q=80'},
    {'name': 'Fresh Lime Soda',     'category': 'drinks', 'price': 70,  'description': 'Refreshing mix of fresh lime juice, sparkling soda, and a pinch of black salt.', 'image_url': 'https://images.unsplash.com/photo-1560508180-03f285f67ded?w=400&q=80'},
    {'name': 'Cold Coffee',         'category': 'drinks', 'price': 120, 'description': 'Blended cold coffee with ice cream and chocolate syrup — rich, thick, and indulgent.', 'image_url': 'https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=400&q=80'},
]

created = 0
for item_data in sample_items:
    obj, was_created = FoodItem.objects.get_or_create(
        name=item_data['name'],
        defaults={
            'category':    item_data['category'],
            'price':       item_data['price'],
            'description': item_data['description'],
            'image_url':   item_data.get('image_url', ''),
            'is_available': True,
        }
    )
    if was_created:
        created += 1
        print(f"  ✅ Created: {obj.name}")
    else:
        print(f"  ⏭️  Already exists: {obj.name}")

print(f"\nDone! {created} new items added. Total items: {FoodItem.objects.count()}")
