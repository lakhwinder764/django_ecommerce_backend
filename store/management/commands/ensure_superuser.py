import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create or update the Django admin superuser from environment variables'

    def handle(self, *args, **options):
        username = os.getenv('ADMIN_USERNAME') or os.getenv('DJANGO_SUPERUSER_USERNAME')
        email = os.getenv('ADMIN_EMAIL') or os.getenv('DJANGO_SUPERUSER_EMAIL', '')
        password = os.getenv('ADMIN_PASSWORD') or os.getenv('DJANGO_SUPERUSER_PASSWORD')

        if not username or not password:
            self.stdout.write(
                self.style.WARNING(
                    'Skipped: set ADMIN_USERNAME and ADMIN_PASSWORD in Render env vars.'
                )
            )
            return

        User = get_user_model()
        user, created = User.objects.get_or_create(
            username=username,
            defaults={'email': email, 'is_staff': True, 'is_superuser': True},
        )

        if not created:
            user.is_staff = True
            user.is_superuser = True
            if email:
                user.email = email

        user.set_password(password)
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f'Created admin user "{username}".'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Updated admin user "{username}".'))
