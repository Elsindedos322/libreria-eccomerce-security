from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import UserProfile

class Command(BaseCommand):
    help = 'Create test users with different roles'

    def handle(self, *args, **options):
        # Crear admin
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@libreria.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('Admin123!')
            admin_user.save()
            UserProfile.objects.create(user=admin_user, role='ADMIN', is_verified=True)
            self.stdout.write(self.style.SUCCESS(f'Admin user created: admin / Admin123!'))
        else:
            self.stdout.write(self.style.WARNING('Admin user already exists'))

        # Crear moderador
        mod_user, created = User.objects.get_or_create(
            username='moderator',
            defaults={
                'email': 'moderator@libreria.com',
                'first_name': 'Moderator',
                'last_name': 'User'
            }
        )
        if created:
            mod_user.set_password('Mod123!')
            mod_user.save()
            UserProfile.objects.create(user=mod_user, role='MODERATOR', is_verified=True)
            self.stdout.write(self.style.SUCCESS(f'Moderator user created: moderator / Mod123!'))
        else:
            self.stdout.write(self.style.WARNING('Moderator user already exists'))

        # Crear usuario normal
        normal_user, created = User.objects.get_or_create(
            username='usuario',
            defaults={
                'email': 'usuario@libreria.com',
                'first_name': 'Usuario',
                'last_name': 'Normal'
            }
        )
        if created:
            normal_user.set_password('User123!')
            normal_user.save()
            UserProfile.objects.create(user=normal_user, role='USER', is_verified=True)
            self.stdout.write(self.style.SUCCESS(f'Normal user created: usuario / User123!'))
        else:
            self.stdout.write(self.style.WARNING('Normal user already exists'))

        # Crear usuario invitado
        guest_user, created = User.objects.get_or_create(
            username='invitado',
            defaults={
                'email': 'invitado@libreria.com',
                'first_name': 'Usuario',
                'last_name': 'Invitado'
            }
        )
        if created:
            guest_user.set_password('Guest123!')
            guest_user.save()
            UserProfile.objects.create(user=guest_user, role='GUEST')
            self.stdout.write(self.style.SUCCESS(f'Guest user created: invitado / Guest123!'))
        else:
            self.stdout.write(self.style.WARNING('Guest user already exists'))

        self.stdout.write(self.style.SUCCESS('Test users setup completed!'))