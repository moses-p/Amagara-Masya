from django.core.management.base import BaseCommand
from children.models import Child, Enrollment
from datetime import date

class Command(BaseCommand):
    help = 'Automatically re-enroll all active children for the new year.'

    def handle(self, *args, **options):
        current_year = date.today().year
        count = 0
        for child in Child.objects.filter(status='active'):
            if not Enrollment.objects.filter(child=child, enrollment_date__year=current_year).exists():
                Enrollment.objects.create(
                    child=child,
                    enrollment_number=f"{child.unique_identifier}-{current_year}",
                    enrollment_date=date.today(),
                    enrollment_type='re_enrollment',
                    status='approved',
                )
                count += 1
        self.stdout.write(self.style.SUCCESS(f'Successfully re-enrolled {count} children for {current_year}.')) 