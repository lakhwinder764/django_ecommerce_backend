from pathlib import Path

from django.core.management.base import BaseCommand
from django.core.files import File

from store.models import Category, Product

BASE_DIR = Path(__file__).resolve().parents[3]
MEDIA_DIR = BASE_DIR / 'media' / 'products'

CATEGORIES = [
    ('Living Room', 'living-room'),
    ('Kitchen', 'kitchen'),
    ('Office', 'office'),
    ('Bedroom', 'bedroom'),
    ('Appliances', 'appliances'),
]

PRODUCTS = [
    {
        'name': 'Plunge dining table',
        'company': 'Ikea',
        'category': 'Living Room',
        'price': 99999,
        'stock': 5,
        'featured': True,
        'stars': 4.5,
        'reviews': 18,
        'colors': ['#000', '#ffb900', '#ff0000'],
        'description': 'Modern dining table perfect for family gatherings.',
        'image': 'table.jpg',
    },
    {
        'name': 'Uttermost pendant',
        'company': 'Uttermost',
        'category': 'Living Room',
        'price': 39999,
        'stock': 12,
        'featured': True,
        'stars': 4.2,
        'reviews': 9,
        'colors': ['#ff0000', '#22a6b3', '#192a56'],
        'description': 'Elegant pendant light for ambient living room lighting.',
        'image': 'bulb.png',
    },
    {
        'name': 'Essence MascaraLash',
        'company': 'Essence',
        'category': 'Bedroom',
        'price': 12999,
        'stock': 20,
        'featured': False,
        'stars': 4.8,
        'reviews': 42,
        'colors': ['#000', '#cd324c'],
        'description': 'Long-lasting mascara for bold lashes.',
        'image': 'oil.png',
    },
    {
        'name': 'Accent floor lamp',
        'company': 'Home Depot',
        'category': 'Living Room',
        'price': 24999,
        'stock': 8,
        'featured': True,
        'stars': 4.0,
        'reviews': 14,
        'colors': ['#000', '#ffb900'],
        'description': 'Stylish floor lamp with adjustable brightness.',
        'image': 'bulb.png',
    },
    {
        'name': 'Wooden study desk',
        'company': 'Ikea',
        'category': 'Office',
        'price': 149999,
        'stock': 3,
        'featured': False,
        'stars': 4.6,
        'reviews': 7,
        'colors': ['#8B4513', '#000'],
        'description': 'Spacious desk with cable management and drawers.',
        'image': 'table.jpg',
    },
    {
        'name': 'Smart LED bulb pack',
        'company': 'Philips',
        'category': 'Appliances',
        'price': 19999,
        'stock': 25,
        'featured': True,
        'stars': 4.3,
        'reviews': 31,
        'colors': ['#fff', '#ffb900'],
        'description': 'Wi-Fi enabled bulbs compatible with voice assistants.',
        'image': 'bulb.png',
    },
    {
        'name': 'Organic coconut oil',
        'company': 'Nature Valley',
        'category': 'Kitchen',
        'price': 8999,
        'stock': 50,
        'featured': False,
        'stars': 4.7,
        'reviews': 88,
        'colors': ['#f5e6c8'],
        'description': 'Cold-pressed virgin coconut oil for cooking and skincare.',
        'image': 'oil.png',
    },
    {
        'name': 'Minimalist coffee table',
        'company': 'West Elm',
        'category': 'Living Room',
        'price': 59999,
        'stock': 6,
        'featured': True,
        'stars': 4.4,
        'reviews': 22,
        'colors': ['#000', '#8B4513'],
        'description': 'Compact coffee table with tempered glass top.',
        'image': 'table.jpg',
    },
    {
        'name': 'Ergonomic office chair',
        'company': 'Steelcase',
        'category': 'Office',
        'price': 189999,
        'stock': 4,
        'featured': False,
        'stars': 4.9,
        'reviews': 56,
        'colors': ['#000', '#2f3640'],
        'description': 'Adjustable lumbar support and breathable mesh back.',
        'image': 'table.jpg',
    },
    {
        'name': 'Queen memory foam mattress',
        'company': 'Sleepwell',
        'category': 'Bedroom',
        'price': 299999,
        'stock': 2,
        'featured': True,
        'stars': 4.5,
        'reviews': 19,
        'colors': ['#fff', '#e8e8e8'],
        'description': 'Pressure-relieving foam with cooling gel layer.',
        'image': 'table.jpg',
    },
    {
        'name': 'Stainless steel blender',
        'company': 'KitchenAid',
        'category': 'Kitchen',
        'price': 44999,
        'stock': 15,
        'featured': False,
        'stars': 4.1,
        'reviews': 27,
        'colors': ['#silver', '#000'],
        'description': 'High-speed blender for smoothies and soups.',
        'image': 'oil.png',
    },
    {
        'name': 'Air purifier HEPA',
        'company': 'Dyson',
        'category': 'Appliances',
        'price': 349999,
        'stock': 7,
        'featured': True,
        'stars': 4.8,
        'reviews': 64,
        'colors': ['#fff', '#000'],
        'description': 'Captures 99.97% of allergens and pollutants.',
        'image': 'bulb.png',
    },
]


class Command(BaseCommand):
    help = 'Seed categories and sample products for the ecommerce store'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Delete existing products and categories before seeding',
        )

    def handle(self, *args, **options):
        if options['clear']:
            Product.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write(self.style.WARNING('Cleared existing catalog data.'))

        category_map = {}
        for name, slug in CATEGORIES:
            category, _ = Category.objects.get_or_create(name=name, defaults={'slug': slug})
            category_map[name] = category

        created = 0
        for data in PRODUCTS:
            image_name = data.pop('image')
            category_name = data.pop('category')
            category = category_map[category_name]

            product, was_created = Product.objects.get_or_create(
                name=data['name'],
                defaults={**data, 'category': category},
            )

            if not was_created:
                for key, value in data.items():
                    setattr(product, key, value)
                product.category = category
                product.save()

            image_path = MEDIA_DIR / image_name
            if image_path.exists() and not product.image:
                with image_path.open('rb') as f:
                    product.image.save(image_name, File(f), save=True)

            if was_created:
                created += 1

        featured_count = Product.objects.filter(featured=True).count()
        self.stdout.write(
            self.style.SUCCESS(
                f'Seed complete: {Product.objects.count()} products '
                f'({featured_count} featured), {created} newly created.'
            )
        )
