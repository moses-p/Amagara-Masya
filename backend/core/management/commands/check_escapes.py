from django.core.management.base import BaseCommand
from core.utils import check_for_escaped_children

class Command(BaseCommand):
    help = 'Check for children who have escaped and notify admins.'

    def handle(self, *args, **options):
        check_for_escaped_children()
        self.stdout.write(self.style.SUCCESS('Checked for escaped children and notified admins if needed.')) 