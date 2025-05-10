from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from core.models import User
from children.models import Child, AcademicRecord, MedicalRecord, BudgetRecord, Tracking

class Command(BaseCommand):
    help = 'Create default user groups and assign permissions.'

    def handle(self, *args, **kwargs):
        # Admin group: all permissions
        admin_group, _ = Group.objects.get_or_create(name='Admin')
        admin_permissions = Permission.objects.all()
        admin_group.permissions.set(admin_permissions)

        # Staff group: limited permissions
        staff_group, _ = Group.objects.get_or_create(name='Staff')
        staff_permissions = []
        for model in [Child, AcademicRecord, MedicalRecord, Tracking]:
            content_type = ContentType.objects.get_for_model(model)
            perms = Permission.objects.filter(content_type=content_type)
            staff_permissions.extend(perms)
        staff_group.permissions.set(staff_permissions)

        # Donor group: read-only permissions for Child, AcademicRecord, BudgetRecord
        donor_group, _ = Group.objects.get_or_create(name='Donor')
        donor_permissions = []
        for model in [Child, AcademicRecord, BudgetRecord]:
            content_type = ContentType.objects.get_for_model(model)
            perms = Permission.objects.filter(content_type=content_type, codename__startswith='view_')
            donor_permissions.extend(perms)
        donor_group.permissions.set(donor_permissions)

        self.stdout.write(self.style.SUCCESS('Default groups and permissions created/updated.')) 