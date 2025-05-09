from django.core.management.base import BaseCommand
from core.models import User
from children.models import Child, Group, Tracking
from django.utils import timezone

class Command(BaseCommand):
    help = 'Creates default users for the system'

    def handle(self, *args, **options):
        # Create admin user
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@amagara.org',
                'first_name': 'Admin',
                'last_name': 'User',
                'user_type': 'admin',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()
            self.stdout.write(self.style.SUCCESS('Created admin user'))

        # Create staff user
        staff, created = User.objects.get_or_create(
            username='staff',
            defaults={
                'email': 'staff@amagara.org',
                'first_name': 'Staff',
                'last_name': 'User',
                'user_type': 'staff',
                'is_staff': True
            }
        )
        if created:
            staff.set_password('staff123')
            staff.save()
            self.stdout.write(self.style.SUCCESS('Created staff user'))

        # Create donor user
        donor, created = User.objects.get_or_create(
            username='donor',
            defaults={
                'email': 'donor@amagara.org',
                'first_name': 'Donor',
                'last_name': 'User',
                'user_type': 'donor'
            }
        )
        if created:
            donor.set_password('donor123')
            donor.save()
            self.stdout.write(self.style.SUCCESS('Created donor user'))

        # Create demo groups
        group_a, _ = Group.objects.get_or_create(name='Group A', year_formed=2007, description='First group formed in 2007')
        group_b, _ = Group.objects.get_or_create(name='Group B', year_formed=2008, description='Second group formed in 2008')

        # Create demo children
        child1, _ = Child.objects.get_or_create(
            first_name='John', last_name='Doe', gender='male', date_of_birth='2010-05-01', unique_identifier='JD2010', group=group_a
        )
        child2, _ = Child.objects.get_or_create(
            first_name='Jane', last_name='Smith', gender='female', date_of_birth='2011-07-15', unique_identifier='JS2011', group=group_b
        )

        # Create tracking record for a missing child
        Tracking.objects.get_or_create(
            child=child1,
            status='missing',
            last_seen=timezone.now(),
            reported_by=admin,
            notes='Last seen at the playground.'
        )

        self.stdout.write(self.style.SUCCESS('Created demo groups, children, and tracking records')) 