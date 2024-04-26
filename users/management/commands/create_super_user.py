from django.core.management import BaseCommand

from users.models import User
import os


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            user_email=os.getenv('SUPERUSER_EMAIL'),
            first_name='Admin',
            is_staff=True,
            is_superuser=True
        )

        user.set_password(os.getenv('SUPERUSER_PASSWORD'))
        user.save()
