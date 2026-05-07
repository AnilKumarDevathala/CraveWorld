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
    {'name': 'Paneer Tikka',        'category': 'starters', 'price': 220, 'description': 'Succulent cottage cheese cubes marinated in spiced yogurt and grilled in a tandoor until perfectly charred.'},
    {'name': 'Veg Spring Rolls',    'category': 'starters', 'price': 150, 'description': 'Crispy golden rolls stuffed with stir-fried vegetables, ginger, and soy sauce.'},
    {'name': 'Chicken Lollipop',    'category': 'starters', 'price': 280, 'description': 'Indo-Chinese classic — chicken wings shaped like lollipops, deep-fried and tossed in chilli sauce.'},
    {'name': 'Hara Bhara Kabab',    'category': 'starters', 'price': 180, 'description': 'Soft, flavourful patties made with spinach, green peas, and paneer, shallow-fried to perfection.'},

    # Main Course
    {'name': 'Butter Chicken',      'category': 'mains', 'price': 320, 'description': 'Tender chicken in a velvety tomato-butter gravy with aromatic spices. Pairs beautifully with naan.'},
    {'name': 'Dal Makhani',         'category': 'mains', 'price': 240, 'description': 'Slow-cooked black lentils simmered overnight with butter and cream — a North Indian staple.'},
    {'name': 'Palak Paneer',        'category': 'mains', 'price': 260, 'description': 'Fresh cottage cheese cubes in a vibrant spinach gravy spiced with cumin and garam masala.'},
    {'name': 'Chicken Biryani',     'category': 'mains', 'price': 350, 'description': 'Fragrant basmati rice layered with marinated chicken, caramelised onions, and saffron.'},
    {'name': 'Veg Fried Rice',      'category': 'mains', 'price': 190, 'description': 'Wok-tossed rice with fresh vegetables, egg, and house soy sauce blend.'},
    {'name': 'Mutton Rogan Josh',   'category': 'mains', 'price': 420, 'description': 'A Kashmiri signature — tender mutton slow-cooked in a rich sauce of whole spices and Kashmiri chillies.'},
    {'name': 'Masala Dosa',         'category': 'mains', 'price': 160, 'description': 'Crispy rice crepe stuffed with spiced mashed potatoes, served with sambar and chutneys.'},

    # Desserts
    {'name': 'Gulab Jamun',         'category': 'desserts', 'price': 90, 'description': 'Soft milk-solid dumplings soaked in rose-cardamom sugar syrup. Best served warm.'},
    {'name': 'Chocolate Lava Cake', 'category': 'desserts', 'price': 180, 'description': 'Warm chocolate cake with a gooey molten centre, served with a scoop of vanilla ice cream.'},
    {'name': 'Mango Kulfi',         'category': 'desserts', 'price': 110, 'description': 'Traditional Indian ice cream made with condensed milk, flavoured with fresh Alphonso mango.'},
    {'name': 'Rasgulla',            'category': 'desserts', 'price': 80, 'description': 'Light, spongy cottage cheese balls simmered in a fragrant sugar syrup.'},

    # Drinks
    {'name': 'Mango Lassi',         'category': 'drinks', 'price': 100, 'description': 'Thick, creamy blend of fresh mango pulp, yogurt, and a hint of cardamom.'},
    {'name': 'Masala Chai',         'category': 'drinks', 'price': 60,  'description': 'Classic Indian spiced tea brewed with ginger, cardamom, cinnamon, and milk.'},
    {'name': 'Fresh Lime Soda',     'category': 'drinks', 'price': 70,  'description': 'Refreshing mix of fresh lime juice, sparkling soda, and a pinch of black salt.'},
    {'name': 'Cold Coffee',         'category': 'drinks', 'price': 120, 'description': 'Blended cold coffee with ice cream and chocolate syrup — rich, thick, and indulgent.'},
]

created = 0
for item_data in sample_items:
    obj, was_created = FoodItem.objects.get_or_create(
        name=item_data['name'],
        defaults={
            'category':    item_data['category'],
            'price':       item_data['price'],
            'description': item_data['description'],
            'is_available': True,
        }
    )
    if was_created:
        created += 1
        print(f"  ✅ Created: {obj.name}")
    else:
        print(f"  ⏭️  Already exists: {obj.name}")

print(f"\nDone! {created} new items added. Total items: {FoodItem.objects.count()}")
