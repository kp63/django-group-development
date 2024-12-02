from django.core.management.base import BaseCommand

from accounts.models import User


class Command(BaseCommand):
    help = 'Make a user an superuser'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, nargs='?')

    def handle(self, *args, **options):
        username = options.get('username')

        if username == None:
            self.stdout.write('Please provide a username: ', ending='')
            username = input().strip()
            if not username:
                self.stderr.write('Username cannot be empty. Please try again.')
                return

        user = User.objects.filter(username=username).first()
        if user == None:
            self.stderr.write(f'User "{username}" not found.')
            return

        if user.is_superuser:
            self.stdout.write(f'User "{user.username}" is already a superuser.')
            return

        user.is_staff = True
        user.is_superuser = True
        user.save()
        self.stdout.write(self.style.SUCCESS(f'User "{user.username}" is now a superuser.'))
