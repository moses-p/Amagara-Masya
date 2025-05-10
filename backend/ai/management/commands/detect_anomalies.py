from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Q
from ...anomaly_detection import AnomalyDetectionSystem
from ...models import Child, Anomaly
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Runs anomaly detection for all active children'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force detection for all children, even if recently checked',
        )

    def handle(self, *args, **options):
        try:
            # Initialize anomaly detection system
            anomaly_system = AnomalyDetectionSystem()

            # Get children to check
            if options['force']:
                children = Child.objects.filter(is_active=True)
            else:
                # Only check children not checked in the last hour
                children = Child.objects.filter(
                    Q(is_active=True) &
                    (Q(last_anomaly_check__isnull=True) |
                     Q(last_anomaly_check__lt=timezone.now() - timezone.timedelta(hours=1)))
                )

            total_children = children.count()
            self.stdout.write(f"Checking {total_children} children for anomalies...")

            # Process each child
            for i, child in enumerate(children, 1):
                self.stdout.write(f"Processing child {i}/{total_children}: {child.name}")
                
                # Detect anomalies
                anomalies = anomaly_system.detect_anomalies(child)
                
                # Update last check timestamp
                child.last_anomaly_check = timezone.now()
                child.save()

                # Log results
                if anomalies:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Found {len(anomalies)} anomalies for {child.name}:"
                        )
                    )
                    for anomaly in anomalies:
                        self.stdout.write(
                            f"  - {anomaly['type']}: {anomaly['description']} "
                            f"(Severity: {anomaly['severity']})"
                        )
                else:
                    self.stdout.write(
                        self.style.SUCCESS(f"No anomalies found for {child.name}")
                    )

            self.stdout.write(self.style.SUCCESS("Anomaly detection completed successfully"))

        except Exception as e:
            logger.error(f"Error running anomaly detection: {str(e)}")
            self.stdout.write(
                self.style.ERROR(f"Error running anomaly detection: {str(e)}")
            ) 