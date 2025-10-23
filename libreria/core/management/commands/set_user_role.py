from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from core.models import UserProfile

class Command(BaseCommand):
    help = "Set or change a user's role (ADMIN, MODERATOR, USER, GUEST). Usage: manage.py set_user_role --username <name> --role <ROLE>"

    def add_arguments(self, parser):
        parser.add_argument('--username', required=True, help='Username of the user to update')
        parser.add_argument('--role', required=True, choices=['ADMIN', 'MODERATOR', 'USER', 'GUEST'], help='Role to assign')

    def handle(self, *args, **options):
        username = options['username']
        role = options['role']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError(f'User {username} does not exist')

        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.role = role
        profile.save()

        self.stdout.write(self.style.SUCCESS(f'Role for user {username} set to {role}'))
