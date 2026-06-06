import re
from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand

from store.models import Category, Product

BASE_DIR = Path(__file__).resolve().parents[3]
SEED_IMAGES_DIR = BASE_DIR / 'store' / 'seed_images'

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
        'colors': ['#2d3436', '#ffb900', '#e17055'],
        'description': 'Modern dining table perfect for family gatherings.',
        'image_file': 'plunge-dining-table.jpg',
    },
    {
        'name': 'Uttermost pendant light',
        'company': 'Uttermost',
        'category': 'Living Room',
        'price': 39999,
        'stock': 12,
        'featured': True,
        'stars': 4.2,
        'reviews': 9,
        'colors': ['#ff7675', '#22a6b3', '#192a56'],
        'description': 'Elegant pendant light for ambient living room lighting.',
        'image_file': 'uttermost-pendant-light.jpg',
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
        'colors': ['#2d3436', '#ffb900'],
        'description': 'Stylish floor lamp with adjustable brightness.',
        'image_file': 'accent-floor-lamp.jpg',
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
        'colors': ['#2d3436', '#8B4513'],
        'description': 'Compact coffee table with tempered glass top.',
        'image_file': 'minimalist-coffee-table.jpg',
    },
    {
        'name': 'Velvet throw pillow set',
        'company': 'Urban Ladder',
        'category': 'Living Room',
        'price': 34999,
        'stock': 30,
        'featured': False,
        'stars': 4.3,
        'reviews': 41,
        'colors': ['#6c5ce7', '#fd79a8', '#00cec9'],
        'description': 'Soft velvet cushions in assorted jewel tones.',
        'image_file': 'velvet-throw-pillow-set.jpg',
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
        'image_file': 'organic-coconut-oil.jpg',
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
        'colors': ['#b2bec3', '#2d3436'],
        'description': 'High-speed blender for smoothies and soups.',
        'image_file': 'stainless-steel-blender.jpg',
    },
    {
        'name': 'Non-stick frying pan',
        'company': 'Prestige',
        'category': 'Kitchen',
        'price': 27999,
        'stock': 22,
        'featured': True,
        'stars': 4.6,
        'reviews': 53,
        'colors': ['#2d3436', '#dfe6e9'],
        'description': 'Induction-ready pan with triple-layer non-stick coating.',
        'image_file': 'non-stick-frying-pan.jpg',
    },
    {
        'name': 'Electric kettle pro',
        'company': 'Philips',
        'category': 'Kitchen',
        'price': 32999,
        'stock': 18,
        'featured': False,
        'stars': 4.5,
        'reviews': 36,
        'colors': ['#ffffff', '#2d3436'],
        'description': 'Rapid-boil kettle with auto shut-off and LED indicator.',
        'image_file': 'electric-kettle-pro.jpg',
    },
    {
        'name': 'Ceramic dinnerware set',
        'company': 'Corelle',
        'category': 'Kitchen',
        'price': 54999,
        'stock': 11,
        'featured': True,
        'stars': 4.4,
        'reviews': 29,
        'colors': ['#ffffff', '#0984e3', '#d63031'],
        'description': '16-piece chip-resistant dinner set for everyday use.',
        'image_file': 'ceramic-dinnerware-set.jpg',
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
        'colors': ['#8B4513', '#2d3436'],
        'description': 'Spacious desk with cable management and drawers.',
        'image_file': 'wooden-study-desk.jpg',
    },
    {
        'name': 'Ergonomic office chair',
        'company': 'Steelcase',
        'category': 'Office',
        'price': 189999,
        'stock': 4,
        'featured': True,
        'stars': 4.9,
        'reviews': 56,
        'colors': ['#2d3436', '#2f3640'],
        'description': 'Adjustable lumbar support and breathable mesh back.',
        'image_file': 'ergonomic-office-chair.jpg',
    },
    {
        'name': 'Wireless ergonomic mouse',
        'company': 'Logitech',
        'category': 'Office',
        'price': 49999,
        'stock': 35,
        'featured': False,
        'stars': 4.7,
        'reviews': 112,
        'colors': ['#2d3436', '#ffffff'],
        'description': 'Silent-click mouse with multi-device Bluetooth pairing.',
        'image_file': 'wireless-ergonomic-mouse.jpg',
    },
    {
        'name': '5-tier bookshelf unit',
        'company': 'Amazon Basics',
        'category': 'Office',
        'price': 89999,
        'stock': 9,
        'featured': False,
        'stars': 4.2,
        'reviews': 33,
        'colors': ['#8B4513', '#2d3436'],
        'description': 'Sturdy engineered-wood shelving for home offices.',
        'image_file': '5-tier-bookshelf-unit.jpg',
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
        'colors': ['#ffffff', '#e8e8e8'],
        'description': 'Pressure-relieving foam with cooling gel layer.',
        'image_file': 'queen-memory-foam-mattress.jpg',
    },
    {
        'name': 'Cotton bedsheet set',
        'company': 'Bombay Dyeing',
        'category': 'Bedroom',
        'price': 42999,
        'stock': 24,
        'featured': False,
        'stars': 4.4,
        'reviews': 67,
        'colors': ['#ffffff', '#74b9ff', '#fd79a8'],
        'description': '300-thread-count breathable cotton sheets with pillowcases.',
        'image_file': 'cotton-bedsheet-set.jpg',
    },
    {
        'name': 'Blackout curtain pair',
        'company': 'Spaces',
        'category': 'Bedroom',
        'price': 37999,
        'stock': 16,
        'featured': False,
        'stars': 4.3,
        'reviews': 45,
        'colors': ['#2d3436', '#636e72', '#0984e3'],
        'description': 'Thermal-insulated curtains that block 99% of sunlight.',
        'image_file': 'blackout-curtain-pair.jpg',
    },
    {
        'name': 'Aromatherapy diffuser',
        'company': 'Essence',
        'category': 'Bedroom',
        'price': 19999,
        'stock': 28,
        'featured': True,
        'stars': 4.8,
        'reviews': 94,
        'colors': ['#ffffff', '#a29bfe'],
        'description': 'Ultrasonic diffuser with 7 LED mood-light modes.',
        'image_file': 'aromatherapy-diffuser.jpg',
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
        'colors': ['#ffffff', '#ffb900'],
        'description': 'Wi-Fi enabled bulbs compatible with voice assistants.',
        'image_file': 'smart-led-bulb-pack.jpg',
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
        'colors': ['#ffffff', '#2d3436'],
        'description': 'Captures 99.97% of allergens and pollutants.',
        'image_file': 'air-purifier-hepa.jpg',
    },
    {
        'name': 'Room humidifier',
        'company': 'Honeywell',
        'category': 'Appliances',
        'price': 89999,
        'stock': 13,
        'featured': False,
        'stars': 4.1,
        'reviews': 38,
        'colors': ['#ffffff', '#74b9ff'],
        'description': 'Ultra-quiet cool-mist humidifier for medium-sized rooms.',
        'image_file': 'room-humidifier.jpg',
    },
]


def slugify(value):
    value = value.lower().strip()
    value = re.sub(r'[^a-z0-9]+', '-', value)
    return value.strip('-')


class Command(BaseCommand):
    help = 'Seed categories and sample products for the ecommerce store'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Delete existing products and categories before seeding',
        )
        parser.add_argument(
            '--skip-images',
            action='store_true',
            help='Skip updating product images',
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
        images_updated = 0
        for data in PRODUCTS:
            image_file = data.pop('image_file')
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

            if not options['skip_images']:
                source_path = SEED_IMAGES_DIR / image_file
                if source_path.exists():
                    if product.image:
                        product.image.delete(save=False)

                    with source_path.open('rb') as image_file_handle:
                        product.image.save(image_file, File(image_file_handle), save=True)
                    images_updated += 1
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f'Missing seed image for "{data["name"]}": {source_path}'
                        )
                    )

            if was_created:
                created += 1

        featured_count = Product.objects.filter(featured=True).count()
        self.stdout.write(
            self.style.SUCCESS(
                f'Seed complete: {Product.objects.count()} products '
                f'({featured_count} featured), {created} newly created, '
                f'{images_updated} images updated.'
            )
        )
