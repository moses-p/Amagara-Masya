from django.core.management.base import BaseCommand
from children.models import Child, Tracking
from core.models import Notification, User
from django.utils import timezone
from datetime import timedelta
from math import radians, cos, sin, asin, sqrt
try:
    from textblob import TextBlob
except ImportError:
    TextBlob = None

class Command(BaseCommand):
    help = 'Detect anomalies in child tracking and notify admins.'

    def handle(self, *args, **options):
        now = timezone.now()
        anomalies = []
        # Example 1: Missing location updates (no update in 1 hour)
        for tracking in Tracking.objects.all():
            if tracking.last_update and (now - tracking.last_update) > timedelta(hours=1):
                anomalies.append(f"Child {tracking.child} has not updated location in over 1 hour.")
        # Example 2: Repeated escapes (more than 2 escapes in last 30 days)
        for child in Child.objects.all():
            escapes = Tracking.objects.filter(child=child, status='escaped', last_update__gte=now-timedelta(days=30)).count()
            if escapes > 2:
                anomalies.append(f"Child {child} has escaped {escapes} times in the last 30 days.")
        # Example 3: Rapid movement (distance > 5km in <10min)
        for child in Child.objects.all():
            records = Tracking.objects.filter(child=child).order_by('-last_update')[:2]
            if len(records) == 2:
                loc1 = records[0].last_known_location
                loc2 = records[1].last_known_location
                t1 = records[0].last_update
                t2 = records[1].last_update
                if loc1 and loc2:
                    lat1, lon1 = map(float, loc1.split(','))
                    lat2, lon2 = map(float, loc2.split(','))
                    R = 6371  # km
                    dlat = radians(lat2 - lat1)
                    dlon = radians(lon2 - lon1)
                    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
                    c = 2 * asin(sqrt(a))
                    distance = R * c
                    if distance > 5 and abs((t1-t2).total_seconds()) < 600:
                        anomalies.append(f"Child {child} moved {distance:.1f}km in less than 10 minutes.")
        # Example 4: Sentiment analysis on notes (if TextBlob is installed)
        if TextBlob:
            for tracking in Tracking.objects.all():
                if tracking.notes:
                    sentiment = TextBlob(tracking.notes).sentiment.polarity
                    if sentiment < -0.5:
                        anomalies.append(f"Negative sentiment in notes for {tracking.child}: '{tracking.notes[:30]}...'")
        # Notify admins
        admins = User.objects.filter(user_type='admin')
        for anomaly in anomalies:
            for admin in admins:
                Notification.objects.create(user=admin, message=f"Anomaly detected: {anomaly}")
        self.stdout.write(self.style.SUCCESS(f"Detected and notified {len(anomalies)} anomalies.")) 